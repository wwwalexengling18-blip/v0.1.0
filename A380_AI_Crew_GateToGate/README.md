# A380 AI Crew Commander (Gate-to-Gate) – MSFS2024 + FBW A380X

Dieses Projekt ist ein **Crew‑Framework** (Captain/PF, FO/PM, Techniker) für eine Gate‑to‑Gate Automatisierung.
Es steuert den **FBW A380X** über die **A380X Flight Deck API** (Custom LVARs / Custom Events / Input Events)
und nutzt optional **WASimCommander** für H‑Events und Calculator‑Code.

Docs (Quelle/Referenz):
- A380X Flight Deck API: https://docs.flybywiresim.com/aircraft/a380x/a380x-api/a380x-flight-deck-api/
- A380X Systems API (Preset Load): https://docs.flybywiresim.com/aircraft/a380x/a380x-api/a380x-systems-api/
- MSFS Input Events: https://docs.flightsimulator.com/html/Content_Configuration/Models/ModelBehaviors/Input_Event_Definitions.htm
- WASimCommander: https://github.com/mpaperno/WASimCommander
- SimBridge: https://docs.flybywiresim.com/tools/simbridge/install-configure/start-simbridge/

## Schnellstart (lokal)
1) Python 3.12 installieren
2) In diesem Ordner:
   - `INSTALL_G2G_K.cmd` ausführen (öffnet mit /k)
   - danach `START_ControlCenter.cmd`

## Wichtig
- „Echte Airline SOPs“ sind oft proprietär. Dieses Projekt liefert ein **SOP‑Framework** + Beispiel‑Flows,
  die du mit deinen Checklisten erweitern kannst.
