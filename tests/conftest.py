import sys
from pathlib import Path

# Make project root importable so `from calculations import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
