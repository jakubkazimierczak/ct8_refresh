__version__ = '0.1.0'

from pathlib import Path
from typing import Final

from rich.console import Console

ROOT_DIR: Final = Path(__file__).parent.parent
DATABASE_PATH: Final = ROOT_DIR / 'accounts.db'
LOG_PATH: Final = ROOT_DIR / 'run.log'
console: Final = Console()
