# Modern Setup.exe (Windows) – Builder

Dieses Verzeichnis erzeugt eine **moderne Setup.exe (GUI)** für Windows.

Workflow:
1) **PyInstaller** baut `A380_AI_Crew_ControlCenter.exe` (ohne Konsole).
2) **Inno Setup 6** baut daraus eine `Setup_A380_AI_Crew_*.exe` (Installer GUI).

Empfohlen: Build über **GitHub Actions** (kein lokales Gefrickel).
