# A380 AI Crew – Gate‑to‑Gate (Scaffold)

Das ist ein **moderner Start** für eine Gate‑to‑Gate‑KI für den FBW A380X in MSFS 2024.
Kernidee: **SimConnect** für Standard‑SimVars/Events + **A380X Flight Deck API** für A380X‑spezifische Controls (Custom LVARs, Custom Events, HTML Events, Input Events/B:).

Quellen:
- SimConnect SDK (MSFS 2024): https://docs.flightsimulator.com/msfs2024/html/6_Programming_APIs/SimConnect/SimConnect_SDK.htm
- A380X Flight Deck API: https://docs.flybywiresim.com/aircraft/a380x/a380x-api/a380x-flight-deck-api/
- A380X Systems API (importierte GitHub‑Docs): https://docs.flybywiresim.com/aircraft/a380x/a380x-api/a380x-systems-api/
- Input Event Definitions (B: Events): https://docs.flightsimulator.com/html/Content_Configuration/Models/ModelBehaviors/Input_Event_Definitions.htm

## Voraussetzungen
1) MSFS 2024 läuft, **FBW A380X** geladen.
2) Eine WASM‑Bridge ist installiert (empfohlen: WASimCommander/WASimModule oder alternativ MobiFlight WASM).

## Installation (modern)
### Dev (schnell)
Empfohlen: `uv` (Python Package Manager). Alternativ geht `pip`.

- `uv sync`  (oder: `python -m venv .venv` + `pip install -e .`)

### Run
- `python -m a380_ai_crew.cli run --plan procedures/g2g.yaml`

## Was hier schon drin ist
- **State Machine Engine** (YAML‑Plan, Guards, Actions)
- **Sim‑Abstraction Layer** (SimConnect + Bridge Adapter Platzhalter)
- **Gate‑to‑Gate Plan** (minimal) in `procedures/g2g.yaml`
- **Diagnose**: `tools/diag_runtime.py`

## Nächste Schritte (die wir als „richtiges Programm“ ausbauen)
- Action‑Map Generator aus FBW‑Dokus (offline cache)
- echte Guards (ready checks) + retry/throttling
- GSX Adapter (Pushback/Boarding optional)
- UI + Installer EXE (alles inkl. Repair/Diagnose)


## Wichtig: Paket-Install (src/ Layout)
Damit `a380_ai_crew` gefunden wird, nutzen wir `pip install -e .` (editable).
Starte dafür `INSTALL_G2G_K.cmd`.


## Cold & Dark mit echten Ladezeiten
Der Plan nutzt die FBW Preset Loader‑LVARs (`A32NX_LOAD_AIRCRAFT_PRESET*`) und wartet auf `*_PROGRESS >= 1.0`.
Zusätzlich gibt es `min_wait` + `sleep_range`, damit es sich realistisch anfühlt.


## One-Click Start (mit /k)
Wenn du es ganz einfach willst: `START_G2G_K.cmd`.
Das macht Install (editable) und startet danach den Plan.
