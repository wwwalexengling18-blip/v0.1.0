from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
import time
import random

from .plan import Plan
from .logger import Logger

@dataclass
class Context:
    sim: Any
    log: Logger

class Engine:
    def __init__(self, plan: Plan, ctx: Context):
        self.plan = plan
        self.ctx = ctx
        self._idx = 0

    def run(self, tick_hz: float = 5.0):
        self.ctx.log.log(f"Plan start: {self.plan.name}")
        dt = 1.0 / max(0.5, tick_hz)
        while self._idx < len(self.plan.steps):
            step = self.plan.steps[self._idx]
            if self._check(step.when):
                self.ctx.log.log(f"STEP {self._idx+1}/{len(self.plan.steps)}: {step.id}")
                for act in step.do:
                    self._do(act)
                self._idx += 1
            time.sleep(dt)
        self.ctx.log.log("Plan finished ✅")

    def _check(self, when: Dict[str, Any]) -> bool:
        tests = when.get("all", [])
        for t in tests:
            if "simvar" in t:
                v = self.ctx.sim.get_simvar(t["simvar"])
                if not _cmp(v, t.get("op", "=="), t.get("value")):
                    return False
            if "lvar" in t:
                v = self.ctx.sim.get_lvar(t["lvar"])
                if not _cmp(v, t.get("op", "=="), t.get("value")):
                    return False
        return True

    def _do(self, act: Dict[str, Any]):
        t = act.get("type")

        if t == "log":
            self.ctx.log.log(str(act.get("msg", "")))
            return

        if t == "sleep":
            time.sleep(float(act.get("sec", 0.2)))
            return

        if t == "sleep_range":
            mn = float(act.get("min", 0.5))
            mx = float(act.get("max", 2.0))
            time.sleep(random.uniform(mn, mx))
            return

        if t == "wait_lvar":
            self._wait_var(kind="lvar", name=act["name"], op=act.get("op", ">="), value=act.get("value", 1),
                           timeout=float(act.get("timeout", 180)), min_wait=float(act.get("min_wait", 0.0)))
            return

        if t == "wait_simvar":
            self._wait_var(kind="simvar", name=act["name"], op=act.get("op", ">="), value=act.get("value", 1),
                           timeout=float(act.get("timeout", 180)), min_wait=float(act.get("min_wait", 0.0)))
            return

        if t == "input_event":
            self.ctx.sim.input_event(act["name"], act.get("value", 1), mode=act.get("mode", "set"))
            return

        if t == "h_event":
            self.ctx.sim.h_event(act["name"])
            return

        if t == "k_event":
            self.ctx.sim.k_event(act["name"], act.get("value", 0))
            return

        if t == "lvar_set":
            self.ctx.sim.set_lvar(act["name"], act.get("value", 0))
            return

        if t == "preset_load":
            # FBW A380X Preset Loader: A32NX_LOAD_AIRCRAFT_PRESET (1..5)
            # Progress: A32NX_LOAD_AIRCRAFT_PRESET_PROGRESS (0.0..1.0)
            # Expedite: A32NX_LOAD_AIRCRAFT_PRESET_EXPEDITE (0/1)
            preset = int(act["preset"])
            expedite = int(act.get("expedite", 0))
            self.ctx.log.log(f"Preset load: {preset} (expedite={expedite})")
            self.ctx.sim.set_lvar("A32NX_LOAD_AIRCRAFT_PRESET_EXPEDITE", expedite)
            self.ctx.sim.set_lvar("A32NX_LOAD_AIRCRAFT_PRESET", preset)
            return

        self.ctx.log.log(f"[WARN] Unknown action type: {t}")

    def _wait_var(self, *, kind: str, name: str, op: str, value, timeout: float, min_wait: float):
        start = time.time()
        min_end = start + min_wait
        while True:
            now = time.time()
            if now - start > timeout:
                raise TimeoutError(f"Timeout waiting for {kind}:{name} {op} {value}")
            v = self.ctx.sim.get_lvar(name) if kind == "lvar" else self.ctx.sim.get_simvar(name)
            ok = _cmp(v, op, value)
            if ok and now >= min_end:
                self.ctx.log.log(f"WAIT OK: {kind}:{name}={v}")
                return
            time.sleep(0.25)

def _cmp(a, op: str, b) -> bool:
    try:
        if op == "==": return a == b
        if op == "!=": return a != b
        if op == ">": return a > b
        if op == ">=": return a >= b
        if op == "<": return a < b
        if op == "<=": return a <= b
    except Exception:
        return False
    return False
