from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import datetime as _dt

def _ts():
    return _dt.datetime.now().isoformat(timespec="seconds")

@dataclass
class Logger:
    path: Path
    jsonl_path: Path | None = None

    def __post_init__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("# Crew Journal\n\n", encoding="utf-8")
        if self.jsonl_path:
            self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.jsonl_path.exists():
                self.jsonl_path.write_text("", encoding="utf-8")

    def log(self, msg: str, role: str = "SYSTEM", step: str | None = None, level: str = "INFO", data: dict | None = None):
        line = f"- [{_ts()}] **{level}** [{role}] {msg}"
        if step:
            line += f" _(step: {step})_"
        if data:
            line += f"\n  - data: `{json.dumps(data, ensure_ascii=False)}`"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        if self.jsonl_path:
            rec = {"ts": _ts(), "level": level, "role": role, "msg": msg, "step": step, "data": data or {}}
            with self.jsonl_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
