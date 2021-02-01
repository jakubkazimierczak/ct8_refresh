__version__ = '0.1.0'

from pathlib import Path

from rich.console import Console


ROOT_DIR = Path(__file__).parent.parent
DATABASE_PATH = ROOT_DIR / 'accounts.db'
LOG_PATH = ROOT_DIR / 'run.log'
console = Console()

