from __future__ import annotations
from pathlib import Path
from ..core.logger import Logger

def run_diagnostics(root: Path, logger: Logger):
    logger.log("Diagnostics: Start", role="SYSTEM")
    wasim_dir = root / "lib" / "wasim"
    dll1 = wasim_dir / "WASimCommander.WASimClient.dll"
    dll2 = wasim_dir / "Ijwhost.dll"
    logger.log(f"WASim DLL dir: {wasim_dir}", role="SYSTEM")
    logger.log(f"WASimClient.dll present: {dll1.exists()}", role="SYSTEM")
    logger.log(f"Ijwhost.dll present: {dll2.exists()}", role="SYSTEM")
    logger.log("Diagnostics: Done", role="SYSTEM")
