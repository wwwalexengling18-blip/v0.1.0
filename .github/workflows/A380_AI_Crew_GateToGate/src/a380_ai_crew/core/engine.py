from __future__ import annotations
from dataclasses import dataclass
import time
from .plan import Plan, Step
from .logger import Logger

@dataclass
class Context:
    sim: any
    log: Logger

class Engine:
    def __init__(self, plan: Plan, ctx: Context):
        self.plan = plan
        self.ctx = ctx

    def run(self, tick_hz: float = 5.0):
        self.ctx.log.log(f"Start Plan: {self.plan.name}", role="SYSTEM")
        dt = 1.0 / max(0.5, tick_hz)

        for ph in self.plan.phases:
            self.ctx.log.log(f"== Phase: {ph.title} ==", role="SYSTEM")
            for step in ph.steps:
                self._run_step(step)
                time.sleep(dt)

        self.ctx.log.log("Plan beendet.", role="SYSTEM")

    def _run_step(self, step: Step):
        raw = step.raw or {}
        role = step.role
        note = step.note or ""
        self.ctx.log.log(f"{step.kind}: {note}".strip(), role=role, step=step.id)

        if step.kind == "ensure_connected":
            self.ctx.sim.ensure_connected()
            return

        if step.kind == "load_preset":
            self.ctx.sim.load_aircraft_preset(
                preset_id=int(raw.get("preset_id", 1)),
                wait_progress=bool(raw.get("wait_progress", True)),
                min_wait_s=int(raw.get("min_wait_s", 0)),
                role=role,
                step=step.id,
            )
            return

        if step.kind == "tech_walkaround":
            self.ctx.sim.tech_walkaround(min_wait_s=int(raw.get("min_wait_s", 0)), role=role, step=step.id)
            return

        if step.kind == "guard":
            ok = self.ctx.sim.check_requirements(raw.get("require", []) or [])
            if not ok:
                self.ctx.log.log("Guard nicht erfüllt → STOP.", role=role, step=step.id, level="ERROR")
                raise RuntimeError("Guard not satisfied")
            return

        if step.kind == "action":
            self.ctx.sim.do_action(str(raw.get("action")), role=role, step=step.id)
            return

        if step.kind == "sleep":
            time.sleep(float(raw.get("seconds", 1)))
            return

        if step.kind == "finish":
            self.ctx.log.log("Fertig ✅", role=role, step=step.id)
            return

        raise ValueError(f"Unknown step kind: {step.kind}")
