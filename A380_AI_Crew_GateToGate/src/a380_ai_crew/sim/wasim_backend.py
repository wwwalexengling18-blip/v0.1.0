from __future__ import annotations
from pathlib import Path
import os
from ..core.logger import Logger

class WASimBackend:
    def __init__(self, base_dir: Path, logger: Logger):
        self.base_dir = base_dir
        self.log = logger
        self.ready = False
        self._client = None

    def _runtime_dir(self) -> Path:
        p = self.base_dir / "lib" / "wasim"
        p.mkdir(parents=True, exist_ok=True)
        return p

    def try_connect(self):
        if self.ready:
            return True
        try:
            import clr  # type: ignore
            import sys
            rt = self._runtime_dir()
            sys.path.append(str(rt))
            os.environ["PATH"] = str(rt) + os.pathsep + os.environ.get("PATH", "")

            clr.AddReference("WASimCommander.WASimClient")
            from WASimCommander import WASimClient  # type: ignore

            self._client = WASimClient()
            self._client.Connect()
            self.ready = True
            self.log.log("WASimCommander connected.", role="SYSTEM")
            return True
        except Exception as e:
            self.ready = False
            self._client = None
            self.log.log(f"WASimCommander not available: {e}", role="SYSTEM")
            return False

    def has_lvar(self, name: str) -> bool:
        if not self.ready:
            return False
        try:
            return bool(self._client.LVarExists(name))
        except Exception:
            return False

    def read_lvar(self, name: str):
        if not self.ready:
            return None
        try:
            return float(self._client.GetLVar(name))
        except Exception:
            return None

    def write_lvar(self, name: str, value: float):
        if not self.ready:
            raise RuntimeError("WASim not ready")
        self._client.SetLVar(name, value)
