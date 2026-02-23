from __future__ import annotations
import argparse
from pathlib import Path
from .core.plan import load_plan
from .core.engine import Engine, Context
from .core.logger import Logger
from .sim.simlayer import SimLayer

def main():
    p = argparse.ArgumentParser(prog="a380-ai-crew")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run a plan YAML")
    run.add_argument("--plan", required=True, help="Path to plan YAML")
    run.add_argument("--tick", type=float, default=None, help="Tick rate (Hz) override")

    diag = sub.add_parser("diag", help="Run diagnostics")

    args = p.parse_args()
    root = Path(".").resolve()
    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    logger = Logger(path=log_dir / "crew_journal.md", jsonl_path=log_dir / "machine_log.jsonl")

    if args.cmd == "diag":
        from .tools.diagnose import run_diagnostics
        run_diagnostics(root=root, logger=logger)
        return

    plan = load_plan(Path(args.plan))
    sim = SimLayer(base_dir=root, logger=logger)
    sim.connect()
    ctx = Context(sim=sim, log=logger)
    tick = args.tick if args.tick else plan.defaults.tick_hz
    Engine(plan=plan, ctx=ctx).run(tick_hz=tick)

if __name__ == "__main__":
    main()
