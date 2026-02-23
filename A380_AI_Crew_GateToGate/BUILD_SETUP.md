# Setup.exe bauen (modern)

## Empfohlen: GitHub Actions (kein lokales Setup nötig)
1) Dieses Projekt in ein GitHub Repo pushen.
2) Tag erstellen: `v0.1.0`
3) Push: `git push origin v0.1.0`
→ GitHub baut automatisch eine **Setup_*.exe** und hängt sie ans Release.

## Lokal (falls du willst)
- Inno Setup 6 installieren
- Python 3.12 installieren
- `pip install -e .` + `pip install pyinstaller`
- `pyinstaller --onefile --noconsole ...`
- `ISCC.exe installer_setup\A380_AI_Crew.iss`
