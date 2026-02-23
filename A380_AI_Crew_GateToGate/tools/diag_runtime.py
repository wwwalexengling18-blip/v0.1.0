from __future__ import annotations
from pathlib import Path
import sys

def main():
    root = Path(".").resolve()
    print("Project:", root)
    print("Python:", sys.version)
    print("Looking for a380x_api/ (WASim backend)…")
    if (root / "a380x_api").exists():
        print("OK: a380x_api folder found.")
    else:
        print("WARN: a380x_api not found. Add it from your installer package.")
    print("Done.")

if __name__ == "__main__":
    main()
