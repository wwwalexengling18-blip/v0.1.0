from __future__ import annotations
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from ..core.logger import Logger

class SimConnectBackend:
    def __init__(self, logger: Logger):
        self.log = logger
        self.sm = None
        self.ar = None
        self.ae = None

    def connect(self):
        self.sm = SimConnect()
        self.ar = AircraftRequests(self.sm, _time=0)
        self.ae = AircraftEvents(self.sm)
        self.log.log("SimConnect connected.", role="SYSTEM")

    def ensure_connected(self):
        if not self.sm:
            self.connect()

    def transmit_event(self, event_name: str):
        if not self.ae:
            raise RuntimeError("SimConnect not ready")
        ev = self.ae.find(event_name)
        ev()

    def get_simvar_bool(self, name: str) -> bool:
        if not self.ar:
            raise RuntimeError("SimConnect not ready")
        try:
            v = self.ar.get(name)
            return bool(int(v)) if v is not None else False
        except Exception:
            return False
