from __future__ import annotations
from pathlib import Path
import time
import yaml
from .simconnect_backend import SimConnectBackend
from .wasim_backend import WASimBackend
from ..core.logger import Logger

class SimLayer:
    def __init__(self, base_dir: Path, logger: Logger):
        self.base_dir = base_dir
        self.log = logger
        self.simconnect = SimConnectBackend(logger=logger)
        self.wasim = WASimBackend(base_dir=base_dir, logger=logger)
        self.actions = self._load_actions()

    def _load_actions(self):
        p = self.base_dir / "configs" / "action_map.yaml"
        obj = yaml.safe_load(p.read_text(encoding="utf-8"))
        return obj.get("actions", {}) if obj else {}

    def connect(self):
        self.simconnect.connect()
        self.wasim.try_connect()

    def ensure_connected(self):
        self.simconnect.ensure_connected()
        self.wasim.try_connect()

    def _pick_lvar(self, candidates):
        candidates = list(candidates or [])
        if self.wasim.ready:
            for c in candidates:
                if self.wasim.has_lvar(c):
                    return c
        return candidates[0] if candidates else None

    def load_aircraft_preset(self, preset_id: int, wait_progress: bool, min_wait_s: int, role: str, step: str):
        act = self.actions.get("load_aircraft_preset", {})
        lvar = self._pick_lvar(act.get("lvar_candidates", []))
        if not lvar:
            raise RuntimeError("No preset LVAR configured")
        if not self.wasim.ready:
            self.log.log("WASim nicht verbunden → Preset-Load braucht Custom LVARs (WASimCommander).", role=role, step=step, level="ERROR")
            raise RuntimeError("WASim required for preset load")

        self.log.log(f"Preset laden: {preset_id} via {lvar}", role=role, step=step)
        self.wasim.write_lvar(lvar, float(preset_id))

        if wait_progress:
            prog = self.actions.get("preset_progress", {})
            prog_lvar = self._pick_lvar(prog.get("lvar_candidates", []))
            if prog_lvar:
                t0 = time.time()
                while True:
                    p = float(self.wasim.read_lvar(prog_lvar) or 0.0)
                    if p >= 0.999:
                        break
                    if time.time() - t0 > 180:
                        raise TimeoutError("Preset load timeout")
                    time.sleep(0.5)
                self.log.log("Preset Progress = 1.0", role=role, step=step)

        if min_wait_s > 0:
            self.log.log(f"Settling wait {min_wait_s}s", role="SYSTEM", step=step)
            time.sleep(min_wait_s)

    def do_action(self, action_name: str, role: str, step: str):
        a = self.actions.get(action_name)
        if not a:
            raise KeyError(f"Action not found: {action_name}")
        if a.get("type") == "simconnect_event":
            self.simconnect.transmit_event(str(a.get("event")))
            self.log.log(f"SimConnect event: {a.get('event')}", role=role, step=step)
            return
        raise ValueError(f"Unsupported action type: {a.get('type')}")

    def check_requirements(self, reqs):
        for r in reqs:
            if r.get("type") == "simvar_bool":
                name = str(r.get("name"))
                want = bool(r.get("value"))
                got = bool(self.simconnect.get_simvar_bool(name))
                if got != want:
                    return False
        return True

    def tech_walkaround(self, min_wait_s: int, role: str, step: str):
        vals = {
            "on_ground": bool(self.simconnect.get_simvar_bool("SIM ON GROUND")),
            "battery_main": bool(self.simconnect.get_simvar_bool("ELECTRICAL MASTER BATTERY")),
            "parking_brake": bool(self.simconnect.get_simvar_bool("BRAKE PARKING POSITION")),
        }
        self.log.log("Techniker: Walkaround/Defects Check (simuliert)", role=role, step=step, data=vals)
        if min_wait_s > 0:
            time.sleep(min_wait_s)
