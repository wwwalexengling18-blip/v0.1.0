from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import time

@dataclass
class Logger:
    path: Path

    def __post_init__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
