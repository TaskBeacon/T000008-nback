from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Minimal task-specific sampler responder template."""

    key: str | None = None
    hit_rate: float = 0.75
    rt_mean_s: float = 0.30
    rt_sd_s: float = 0.05
    rt_min_s: float = 0.12

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.hit_rate = max(0.0, min(1.0, float(self.hit_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        if float(rng.random()) > self.hit_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "miss"})

        chosen_key = self.key if self.key in valid_keys else valid_keys[0]
        rt = max(self.rt_min_s, float(rng.normal(self.rt_mean_s, self.rt_sd_s)))
        return Action(key=chosen_key, rt_s=rt, meta={"source": "task_sampler", "outcome": "hit"})


    def on_feedback(self, fb) -> None:
        return

    def end_session(self) -> None:
        self._rng = None

