"""Synthetic counterexamples for source-review findings; no provider execution."""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from skillopt.envs.skilltask import rollout
from skillopt.model import claude_backend
from skillopt_sleep import backend, staging
from skillopt_sleep.types import SleepReport, TaskRecord


@pytest.mark.parametrize('scheme', ['Bearer', 'Basic'])
def test_json_authorization_is_redacted(scheme):
    credential = 'SyntheticCredential42'
    text = json.dumps({'Authorization': f'{scheme} {credential}'})
    assert credential not in staging.redact_secrets(text)


def test_staging_report_redacts_both_formats(tmp_path):
    secret = 'SyntheticCredential42'
    report = SleepReport(night=1, project=str(tmp_path), notes=[f'password={secret}'])
    out = staging.write_staging(
        str(tmp_path), report=report, proposed_skill=None, proposed_memory=None,
        live_skill_path=str(tmp_path/'SKILL.md'), live_memory_path=str(tmp_path/'CLAUDE.md'),
        report_md=f'password={secret}',
    )
    from pathlib import Path
    assert secret not in (Path(out)/'report.json').read_text()
    assert secret not in (Path(out)/'report.md').read_text()


def test_staging_alias_rejected_before_creation(tmp_path):
    project = tmp_path/'project'
    outside = tmp_path/'outside'
    project.mkdir()
    outside.mkdir()
    (project/'.skillopt-sleep').symlink_to(outside, target_is_directory=True)
    with pytest.raises(staging.StagingError):
        staging.new_staging_dir(str(project))
    assert not (outside/'staging').exists()


def test_cli_failure_is_not_cached(monkeypatch):
    instance = backend.CliBackend()
    replies = iter(['', 'recovered'])
    monkeypatch.setattr(instance, '_call', lambda *a, **kw: next(replies))
    assert instance._cached_call('attempt:k', 'prompt') == ''
    assert instance._cached_call('attempt:k', 'prompt') == 'recovered'
    assert instance._cached_call('attempt:k', 'prompt') == 'recovered'


def test_extract_json_stops_at_first_valid_value():
    assert backend._extract_json('Result: {"score":0.9} Debug: {"trace":1}', 'object') == {'score':0.9}


@pytest.mark.parametrize('reference,response', [('42','142'), ('-5','5'), ('5','-5')])
def test_exact_scores_preserve_numeric_boundaries(reference, response):
    assert backend.exact_score(reference, response) == 0.0


def test_exact_scoring_keeps_supported_wrappers():
    assert backend.exact_score('42', '<answer>42</answer>') == 1.0
    assert backend.exact_score('arXiv:1706.03762', 'the id is arXiv:1706.03762 ok') == 1.0


@pytest.mark.parametrize('score', [100, -1, 'NaN', 'Infinity', True])
def test_cli_judge_rejects_invalid_reward(score, monkeypatch):
    instance = backend.CliBackend()
    monkeypatch.setattr(instance, '_call', lambda *a, **kw: json.dumps({'score':score}))
    hard, soft, reason = instance.judge(TaskRecord(id='synthetic', project='.', intent='test'), 'answer')
    assert (hard, soft) == (0.0, 0.0)
    assert 'parse' in reason or 'invalid' in reason


def test_mock_zero_edit_budget_returns_no_edits():
    task = TaskRecord(id='synthetic', project='.', intent='test', tags=['rule:wrap-answer'])
    assert backend.MockBackend().reflect([(task, None)], [], '', '', edit_budget=0,
                                        evolve_skill=True, evolve_memory=False) == []


def test_skilltask_judge_failure_keeps_batch_alive(tmp_path, monkeypatch):
    monkeypatch.setattr(rollout, 'chat_target', lambda **kw: ('answer', {}))
    def failed_judge(**kw):
        raise RuntimeError('synthetic judge failure')
    monkeypatch.setattr(rollout, 'chat_optimizer', failed_judge)
    results = rollout.run_batch(items=[{'id':'one','question':'question','rubric':'rubric'}],
                                skill_content='synthetic', out_root=str(tmp_path))
    assert len(results) == 1
    assert results[0]['hard'] == 0
    assert 'judge' in results[0]['fail_reason']


def test_claude_structured_output_uses_json_schema(monkeypatch):
    seen = []
    def fake_run(command, **kwargs):
        seen.extend(command)
        return SimpleNamespace(returncode=0, stdout=json.dumps({'type':'result','structured_output':{'content':'answer','tool_calls':[]}}), stderr='')
    monkeypatch.setattr(claude_backend.subprocess, 'run', fake_run)
    claude_backend._run_claude_print(system='synthetic', prompt='synthetic', model='',
                                   tools=None, tool_choice=None, return_message=True, timeout=1)
    assert '--json-schema' in seen
    assert '--schema' not in seen


@pytest.mark.parametrize('factory', [backend.ClaudeCliBackend, backend.CodexCliBackend, backend.CopilotCliBackend])
def test_tool_names_cannot_overwrite_outside_files(factory, tmp_path, monkeypatch):
    victim = tmp_path/'sentinel'
    victim.write_text('preserve me', encoding='utf-8')
    monkeypatch.setattr(backend.subprocess, 'run', lambda *a, **kw: SimpleNamespace(returncode=0, stdout='answer', stderr=''))
    instance = factory()
    task = TaskRecord(id='synthetic', project=str(tmp_path), intent='synthetic')
    with pytest.raises(ValueError, match='tool'):
        instance.attempt_with_tools(task, '', '', [str(victim)])
    assert victim.read_text() == 'preserve me'


def test_responses_endpoint_guard_precedes_credentials(monkeypatch):
    instance = backend.AzureResponsesBackend(endpoints=['https://example.invalid/'])
    def forbidden():
        pytest.fail('credential provider reached before endpoint validation')
    monkeypatch.setattr(instance, '_get_provider', forbidden)
    with pytest.raises(ValueError, match='endpoint'):
        instance._client_for(instance.endpoints[0])


def test_copilot_text_calls_have_no_tools_or_inherited_approval(monkeypatch):
    seen = {}
    def fake_run(command, **kwargs):
        seen.update(command=command, **kwargs)
        return SimpleNamespace(returncode=0, stdout='', stderr='')
    monkeypatch.setattr(backend.subprocess, 'run', fake_run)
    monkeypatch.setenv('COPILOT_ALLOW_ALL', '1')
    backend.CopilotCliBackend()._call('synthetic')
    assert '--available-tools=' in seen['command']
    assert '--allow-all-tools' not in seen['command']
    assert 'COPILOT_ALLOW_ALL' not in seen['env']


@pytest.mark.parametrize('factory', [backend.ClaudeCliBackend, backend.CodexCliBackend, backend.CopilotCliBackend])
def test_failed_cli_output_is_not_an_answer(factory, monkeypatch):
    def fake_run(command, **kwargs):
        from pathlib import Path
        if '-o' in command:
            Path(command[command.index('-o')+1]).write_text('plausible partial answer', encoding='utf-8')
        return SimpleNamespace(returncode=2, stdout='plausible partial answer', stderr='synthetic failure')
    monkeypatch.setattr(backend.subprocess, 'run', fake_run)
    instance = factory()
    # Avoid the Codex retry loop; test its single-attempt status boundary.
    call = getattr(instance, '_call_once', instance._call)
    assert call('synthetic') == ''
    assert instance.last_call_error


@pytest.mark.parametrize('factory', [backend.ClaudeCliBackend, backend.CodexCliBackend, backend.CopilotCliBackend])
def test_failed_tool_execution_never_credits_partial_artifacts(factory, tmp_path, monkeypatch):
    def fake_run(command, **kwargs):
        from pathlib import Path
        work = Path(kwargs['cwd'])
        (work/'_tool_calls.log').write_text('search\n', encoding='utf-8')
        (work/'_last.txt').write_text('partial answer', encoding='utf-8')
        return SimpleNamespace(returncode=2, stdout='partial answer', stderr='synthetic failure')
    monkeypatch.setattr(backend.subprocess, 'run', fake_run)
    task = TaskRecord(id='synthetic', project=str(tmp_path), intent='synthetic')
    instance = factory()
    assert instance.attempt_with_tools(task, '', '', ['search']) == ('', [])
    assert instance.last_call_error
