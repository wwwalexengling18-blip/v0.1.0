from __future__ import annotations
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from a380_ai_crew.core.plan import load_plan
from a380_ai_crew.core.engine import Engine, Context
from a380_ai_crew.core.logger import Logger
from a380_ai_crew.sim.simlayer import SimLayer

APP_NAME = "A380 AI Crew – Control Center"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("920x560")
        self.minsize(860, 520)

        self.plan_path = tk.StringVar(value=str(Path("src/a380_ai_crew/procedures/g2g.yaml").resolve()))
        self.tick = tk.DoubleVar(value=5.0)

        self._worker: threading.Thread | None = None

        self._build()

    def _build(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text=APP_NAME, font=("Segoe UI", 14, "bold")).pack(anchor="w")

        row = ttk.Frame(frm)
        row.pack(fill="x", pady=(12, 6))
        ttk.Label(row, text="Plan (YAML):").pack(side="left")
        ttk.Entry(row, textvariable=self.plan_path).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(row, text="Durchsuchen…", command=self.browse).pack(side="left")

        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=(0, 10))
        ttk.Label(row2, text="Tick (Hz):").pack(side="left")
        ttk.Entry(row2, textvariable=self.tick, width=8).pack(side="left", padx=8)
        self.btn_run = ttk.Button(row2, text="Gate‑to‑Gate starten", command=self.run_plan)
        self.btn_run.pack(side="left", padx=(8,0))
        ttk.Button(row2, text="Stop (soft)", command=self.soft_stop).pack(side="left", padx=(8,0))

        self.status = tk.StringVar(value="Bereit")
        ttk.Label(frm, textvariable=self.status).pack(anchor="w")

        self.log = tk.Text(frm, height=18, wrap="word")
        self.log.pack(fill="both", expand=True, pady=(10,0))
        self._log("Bereit. Starte MSFS 2024, lade FBW A380X, dann klicke Start.\n")

    def _log(self, s: str):
        self.log.insert("end", s + ("\n" if not s.endswith("\n") else ""))
        self.log.see("end")
        self.update_idletasks()

    def browse(self):
        p = filedialog.askopenfilename(title="Plan wählen", filetypes=[("YAML", "*.yaml *.yml"), ("All", "*.*")])
        if p:
            self.plan_path.set(p)

    def run_plan(self):
        if self._worker and self._worker.is_alive():
            return
        self.btn_run.configure(state="disabled")
        self.status.set("Läuft…")
        self._worker = threading.Thread(target=self._run_worker, daemon=True)
        self._worker.start()
        self.after(250, self._poll)

    def _poll(self):
        if self._worker and self._worker.is_alive():
            self.after(250, self._poll)
            return
        self.btn_run.configure(state="normal")
        self.status.set("Fertig ✅")

    def soft_stop(self):
        messagebox.showinfo("Stop", "Soft-Stop kommt als nächster Ausbau (State Machine Abort).")

    def _run_worker(self):
        try:
            root = Path(".").resolve()
            log_path = root / "logs" / "g2g_gui.log"
            logger = Logger(path=log_path)
            self._log(f"Log: {log_path}")

            sim = SimLayer(base_dir=root)
            self._log("Connecting SimConnect…")
            sim.connect()
            self._log("SimConnect OK.")

            plan = load_plan(Path(self.plan_path.get()))
            ctx = Context(sim=sim, log=logger)

            # Mirror logger output to GUI by wrapping
            orig_log = logger.log
            def both(msg: str):
                orig_log(msg)
                self.after(0, lambda: self._log(msg))
            logger.log = both  # type: ignore

            Engine(plan=plan, ctx=ctx).run(tick_hz=float(self.tick.get()))
        except Exception as e:
            self.after(0, lambda: (self.status.set("Fehler ❌"), self._log(f"ERROR: {e}")))

def main():
    app = App()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app.mainloop()

if __name__ == "__main__":
    main()
