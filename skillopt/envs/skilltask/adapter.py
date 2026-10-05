"""SkillOpt adapter for the generic ``skilltask`` env."""
from __future__ import annotations

from skillopt.datasets.base import BatchSpec
from skillopt.envs.base import EnvAdapter
from skillopt.envs.skilltask.dataloader import SkillTaskDataLoader
from skillopt.envs.skilltask.rollout import DEFAULT_ANSWER_PREAMBLE, run_batch


class SkillTaskAdapter(EnvAdapter):
    """Train any skill document against a task set graded by match or LLM judge."""

    def __init__(
        self,
        split_dir: str = "",
        data_path: str = "",
        split_mode: str = "ratio",
        split_ratio: str = "5:3:2",
        split_seed: int = 42,
        split_output_dir: str = "",
        workers: int = 4,
        analyst_workers: int = 4,
        failure_only: bool = False,
        minibatch_size: int = 8,
        edit_budget: int = 4,
        seed: int = 42,
        limit: int = 0,
        max_completion_tokens: int = 4096,
        grader: str = "auto",
        pass_threshold: float = 0.7,
        judge_max_tokens: int = 1024,
        answer_preamble: str | None = None,
    ) -> None:
        self.workers = workers
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.max_completion_tokens = int(max_completion_tokens)
        self.grader = str(grader or "auto").lower()
        if self.grader not in {"auto", "exact", "contains", "judge"}:
            raise ValueError(f"skilltask grader must be auto|exact|contains|judge, got {grader!r}")
        self.pass_threshold = float(pass_threshold)
        self.judge_max_tokens = int(judge_max_tokens)
        # None = default note; "" = send the task input unchanged.
        self.answer_preamble = DEFAULT_ANSWER_PREAMBLE if answer_preamble is None else str(answer_preamble)
        self.dataloader = SkillTaskDataLoader(
            split_dir=split_dir,
            data_path=data_path,
            split_mode=split_mode,
            split_ratio=split_ratio,
            split_seed=split_seed,
            split_output_dir=split_output_dir,
            seed=seed,
            limit=limit,
        )

    def setup(self, cfg: dict) -> None:
        super().setup(cfg)
        self.dataloader.setup(cfg)

    def get_dataloader(self):
        return self.dataloader

    def build_env_from_batch(self, batch: BatchSpec, **kwargs):
        return list(batch.payload or [])

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        batch = self.dataloader.build_train_batch(batch_size=batch_size, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        batch = self.dataloader.build_eval_batch(env_num=env_num, split=split, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs) -> list[dict]:
        return run_batch(
            items=list(env_manager),
            skill_content=skill_content,
            out_root=out_dir,
            workers=self.workers,
            max_completion_tokens=self.max_completion_tokens,
            default_grader=self.grader,
            pass_threshold=self.pass_threshold,
            judge_max_tokens=self.judge_max_tokens,
            answer_preamble=self.answer_preamble,
        )

    def get_task_types(self) -> list[str]:
        seen: list[str] = []
        for item in self.dataloader.train_items + self.dataloader.val_items + self.dataloader.test_items:
            task_type = str(item.get("task_type") or "skilltask")
            if task_type not in seen:
                seen.append(task_type)
        return seen or ["skilltask"]
