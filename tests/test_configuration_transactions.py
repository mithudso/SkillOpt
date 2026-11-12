"""Synthetic checks for rejected settings and endpoint/key consistency."""
from __future__ import annotations

import io
import os
from dataclasses import fields

import pytest

from skillopt.model import backend_config, qwen_backend


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch):
    monkeypatch.setattr(os, 'environ', dict(os.environ))
    for name, value in list(vars(backend_config).items()):
        if name.isupper() and isinstance(value, (str, int, bool)):
            monkeypatch.setattr(backend_config, name, value)
    snapshots = [(config, {field.name:getattr(config,field.name) for field in fields(config)})
                 for config in (qwen_backend.OPTIMIZER_CONFIG,qwen_backend.TARGET_CONFIG)]
    yield
    for config, snapshot in snapshots:
        for name,value in snapshot.items():
            setattr(config,name,value)


@pytest.mark.parametrize('role', ['optimizer','target'])
def test_invalid_backend_does_not_change_active_role(role):
    setter = getattr(backend_config,f'set_{role}_backend')
    getter = getattr(backend_config,f'get_{role}_backend')
    previous = getter()
    with pytest.raises(ValueError,match='Unsupported'):
        setter('synthetic-unsupported-backend')
    assert getter() == previous


def test_rejected_qwen_configuration_is_atomic():
    before = {field.name:getattr(qwen_backend.OPTIMIZER_CONFIG,field.name)
              for field in fields(qwen_backend.OPTIMIZER_CONFIG)}
    environment = dict(os.environ)
    with pytest.raises(ValueError):
        qwen_backend.configure_qwen_chat(base_url='https://synthetic.invalid/v1', target_temperature='invalid')
    assert {field.name:getattr(qwen_backend.OPTIMIZER_CONFIG,field.name)
            for field in fields(qwen_backend.OPTIMIZER_CONFIG)} == before
    assert dict(os.environ) == environment


def test_qwen_request_keeps_endpoint_and_credential_from_one_snapshot(monkeypatch):
    qwen_backend.configure_qwen_chat(target_base_url='https://first.invalid/v1',target_api_key='synthetic-first-key')
    original = qwen_backend._chat_url
    captured = []
    def interleaved_url(config):
        qwen_backend.configure_qwen_chat(target_base_url='https://second.invalid/v1',target_api_key='synthetic-second-key')
        return original(config)
    monkeypatch.setattr(qwen_backend,'_chat_url',interleaved_url)
    def fake_open(request, **kwargs):
        captured.append((request.full_url,request.get_header('Authorization')))
        return io.BytesIO(b'{}')
    monkeypatch.setattr(qwen_backend.urllib.request,'urlopen',fake_open)
    qwen_backend._post_chat_completion({},1,qwen_backend.TARGET_CONFIG)
    assert captured == [('https://first.invalid/v1/chat/completions','Bearer synthetic-first-key')]


@pytest.mark.parametrize('value', ['NaN','Infinity','-Infinity'])
def test_qwen_rejects_nonfinite_temperature(value):
    with pytest.raises(ValueError,match='finite'):
        qwen_backend.configure_qwen_chat(target_temperature=value)


def test_qwen_legacy_thinking_update_persists_wire_mode():
    qwen_backend.configure_qwen_chat(target_thinking_mode='enabled')
    qwen_backend.configure_qwen_chat(target_enable_thinking=False)
    assert qwen_backend.TARGET_CONFIG.thinking_mode == qwen_backend._resolve_thinking_mode('target')
