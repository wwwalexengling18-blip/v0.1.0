from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
import sys

# SimConnect Python package varies by wrapper. This file is a placeholder for your current one.
try:
    from SimConnect import SimConnect, AircraftRequests  # type: ignore
except Exception:
    SimConnect = None
    AircraftRequests = None

@dataclass
class SimLayer:
    # You can swap this later to a proper adapter class.
    base_dir: Path

    def __post_init__(self):
        self._sc = None
        self._aq = None
        self._wasim = None

    def connect(self):
        # SimConnect
        if SimConnect is None:
            raise RuntimeError("SimConnect Python package not available.")
        self._sc = SimConnect()
        self._aq = AircraftRequests(self._sc, _time=0)

    # --- Standard simvars via SimConnect ---
    def get_simvar(self, name: str):
        if not self._aq:
            raise RuntimeError("SimConnect not connected.")
        # AircraftRequests exposes many vars as attributes; for generic names, use .get()
        try:
            v = getattr(self._aq, name)
            return v
        except Exception:
            try:
                return self._aq.get(name)
            except Exception:
                return None

    # --- A380X: bridge (WASimCommander) ---
    def ensure_wasim(self):
        if self._wasim is not None:
            return
        from a380x_api.wasim_backend import WASimBackend  # your existing module from earlier steps
        w = WASimBackend(base_dir=self.base_dir)
        w.connect()
        self._wasim = w

    def get_lvar(self, name: str):
        self.ensure_wasim()
        return self._wasim.get_lvar(name)

    def set_lvar(self, name: str, value: float | int):
        self.ensure_wasim()
        self._wasim.set_lvar(name, value)

    def h_event(self, name: str):
        self.ensure_wasim()
        self._wasim.exec_calc(f"1 (>H:{name})")

    def k_event(self, name: str, param: float | int = 0):
        self.ensure_wasim()
        self._wasim.exec_calc(f"{float(param)} (>K:{name})")

    def input_event(self, preset: str, value: float | int = 1, mode: str = "set"):
        # MSFS Input Events use B: variables / preset IDs (see docs)
        # Example in docs: ( >B:Sound_COM1_Volume_Inc )  /  50 (>B:Sound_COM1_Volume_Set)
        self.ensure_wasim()
        if mode == "raw":
            self._wasim.exec_calc(f"{float(value)} (>B:{preset})")
        else:
            self._wasim.exec_calc(f"{float(value)} (>B:{preset}_Set)")
