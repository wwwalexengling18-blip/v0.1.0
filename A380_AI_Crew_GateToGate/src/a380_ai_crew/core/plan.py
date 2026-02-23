from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Defaults:
    tick_hz: float = 5.0
    retry: int = 2
    timeout_s: int = 45

@dataclass
class Step:
    id: str
    role: str
    kind: str
    note: str | None = None
    raw: dict | None = None

@dataclass
class Phase:
    id: str
    title: str
    steps: list[Step]

@dataclass
class Plan:
    version: int
    name: str
    description: str
    defaults: Defaults
    phases: list[Phase]

def load_plan(path: Path) -> Plan:
    obj = yaml.safe_load(path.read_text(encoding="utf-8"))
    d = obj.get("defaults", {}) or {}
    defaults = Defaults(
        tick_hz=float(d.get("tick_hz", 5.0)),
        retry=int(d.get("retry", 2)),
        timeout_s=int(d.get("timeout_s", 45)),
    )
    phases: list[Phase] = []
    for ph in obj.get("phases", []):
        steps: list[Step] = []
        for s in ph.get("steps", []):
            steps.append(Step(
                id=str(s.get("id")),
                role=str(s.get("role", "SYSTEM")),
                kind=str(s.get("kind")),
                note=s.get("note"),
                raw=s,
            ))
        phases.append(Phase(id=str(ph.get("id")), title=str(ph.get("title")), steps=steps))
    return Plan(
        version=int(obj.get("version", 1)),
        name=str(obj.get("name", "Plan")),
        description=str(obj.get("description", "")),
        defaults=defaults,
        phases=phases,
    )
