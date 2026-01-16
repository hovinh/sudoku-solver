import sys
from pathlib import Path

# Add the project root directory to sys.path for module resolution
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))
