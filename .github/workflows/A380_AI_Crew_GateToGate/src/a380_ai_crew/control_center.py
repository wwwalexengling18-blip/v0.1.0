from __future__ import annotations
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .core.plan import load_plan
from .core.engine import Engine, Context
from .core.logger import Logger
from .sim.simlayer import SimLayer
from .tools.diagnose import run_diagnostics

APP = "A380 AI Crew Commander (MSFS2024 + FBW A380X)"

class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP)
        self.geometry("980x620")
        self.minsize(920, 560)

        self.plan_path = tk.StringVar(value=str((Path("configs") / "gate_to_gate.yaml").resolve()))
        self.tick = tk.DoubleVar(value=5.0)

        self._thread = None
        self._build()

    def _build(self):
        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text=APP, font=("Segoe UI", 14, "bold")).pack(anchor="w")

        top = ttk.Frame(main)
        top.pack(fill="x", pady=(10, 6))
        ttk.Label(top, text="Plan (YAML):").pack(side="left")
        ttk.Entry(top, textvariable=self.plan_path).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(top, text="Durchsuchen…", command=self._browse).pack(side="left")

        bar = ttk.Frame(main)
        bar.pack(fill="x", pady=(4, 8))
        ttk.Label(bar, text="Tick (Hz):").pack(side="left")
        ttk.Entry(bar, textvariable=self.tick, width=8).pack(side="left", padx=8)

        self.btn_run = ttk.Button(bar, text="Gate‑to‑Gate starten", command=self._start_run)
        self.btn_run.pack(side="left", padx=(8, 0))

        ttk.Button(bar, text="Diagnose", command=self._diag).pack(side="left", padx=8)
        ttk.Button(bar, text="Logs öffnen", command=self._open_logs).pack(side="left")

        self.state = tk.StringVar(value="Bereit")
        ttk.Label(main, textvariable=self.state).pack(anchor="w")

        self.prog = ttk.Progressbar(main, mode="indeterminate")
        self.prog.pack(fill="x", pady=(6, 6))

        self.txt = tk.Text(main, height=22, wrap="word")
        self.txt.pack(fill="both", expand=True)
        self._log("Bereit. Starte MSFS 2024, lade FBW A380X, dann Start.\n")

    def _log(self, s: str):
        self.txt.insert("end", s + ("" if s.endswith("\n") else "\n"))
        self.txt.see("end")
        self.update_idletasks()

    def _browse(self):
        p = filedialog.askopenfilename(title="Plan wählen", filetypes=[("YAML", "*.yaml *.yml"), ("All", "*.*")])
        if p:
            self.plan_path.set(p)

    def _open_logs(self):
        try:
            logs = Path("logs").resolve()
            logs.mkdir(exist_ok=True)
            import os
            os.startfile(str(logs))
        except Exception as e:
            messagebox.showerror("Logs", str(e))

    def _diag(self):
        logs = Path("logs").resolve()
        logs.mkdir(exist_ok=True)
        logger = Logger(path=logs / "crew_journal.md", jsonl_path=logs / "machine_log.jsonl")
        run_diagnostics(root=Path(".").resolve(), logger=logger)
        self._log("Diagnose geschrieben in logs/crew_journal.md")

    def _start_run(self):
        if self._thread and self._thread.is_alive():
            return
        self.btn_run.configure(state="disabled")
        self.state.set("Läuft…")
        self.prog.start(10)
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        self.after(200, self._poll)

    def _poll(self):
        if self._thread and self._thread.is_alive():
            self.after(200, self._poll)
            return
        self.prog.stop()
        self.btn_run.configure(state="normal")
        if self.state.get() == "Läuft…":
            self.state.set("Fertig ✅")

    def _worker(self):
        try:
            root = Path(".").resolve()
            logs = root / "logs"
            logs.mkdir(exist_ok=True)
            logger = Logger(path=logs / "crew_journal.md", jsonl_path=logs / "machine_log.jsonl")

            orig = logger.log
            def both(msg, role="SYSTEM", step=None, level="INFO", data=None):
                orig(msg, role=role, step=step, level=level, data=data)
                self.after(0, lambda: self._log(f"[{level}] [{role}] {msg}"))
            logger.log = both  # type: ignore

            sim = SimLayer(base_dir=root, logger=logger)
            logger.log("Connect SimConnect…", role="SYSTEM")
            sim.connect()

            plan = load_plan(Path(self.plan_path.get()))
            ctx = Context(sim=sim, log=logger)
            Engine(plan=plan, ctx=ctx).run(tick_hz=float(self.tick.get()))
            self.after(0, lambda: self.state.set("Fertig ✅"))
        except Exception as e:
            self.after(0, lambda: self.state.set("Fehler ❌"))
            self.after(0, lambda: self._log(f"ERROR: {e}"))

def main():
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    AppUI().mainloop()

if __name__ == "__main__":
    main()
