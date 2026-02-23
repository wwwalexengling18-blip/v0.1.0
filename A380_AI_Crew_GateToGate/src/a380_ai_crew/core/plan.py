from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

@dataclass
class Step:
    id: str
    when: Dict[str, Any]
    do: List[Dict[str, Any]]

@dataclass
class Plan:
    name: str
    steps: List[Step]

def load_plan(path: Path) -> Plan:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    name = data.get("name", path.stem)
    steps = []
    for s in data.get("steps", []):
        steps.append(Step(id=s["id"], when=s.get("when", {}), do=s.get("do", [])))
    return Plan(name=name, steps=steps)
