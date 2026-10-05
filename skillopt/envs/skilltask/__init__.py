"""Generic task-set benchmark for optimizing an arbitrary skill document.

Each task is one prompt plus either an ``expected`` answer (string match) or a
``rubric`` (LLM judge). The skill under training is the target's system prompt.
Fork-local addition; see ``scripts/skillopt_skill.py`` for the launcher.
"""
