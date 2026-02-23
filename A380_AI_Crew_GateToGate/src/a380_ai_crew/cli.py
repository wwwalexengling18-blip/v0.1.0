from __future__ import annotations
import argparse
from pathlib import Path

from a380_ai_crew.core.plan import load_plan
from a380_ai_crew.core.engine import Engine, Context
from a380_ai_crew.core.logger import Logger
from a380_ai_crew.sim.simlayer import SimLayer

def main():
    ap = argparse.ArgumentParser(prog="a380-ai")
    sub = ap.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run a gate-to-gate plan")
    run.add_argument("--plan", default="src/a380_ai_crew/procedures/g2g.yaml")
    run.add_argument("--tick", type=float, default=5.0)

    args = ap.parse_args()

    if args.cmd == "run":
        plan_path = Path(args.plan).resolve()
        plan = load_plan(plan_path)

        root = Path(".").resolve()
        log = Logger(path=root / "logs" / "g2g.log")

        sim = SimLayer(base_dir=root)
        log.log("Connecting SimConnect…")
        sim.connect()
        log.log("SimConnect OK.")

        ctx = Context(sim=sim, log=log)
        Engine(plan=plan, ctx=ctx).run(tick_hz=args.tick)

if __name__ == "__main__":
    main()
