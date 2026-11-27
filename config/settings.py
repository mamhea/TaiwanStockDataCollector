from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
EXPORT_DIR = DATA_DIR / "exports"
LOG_DIR = BASE_DIR / "logs"


# Database configuration
DATABASE_PATH = DATABASE_DIR / "taiwan_stock.db"


# API configuration
REQUEST_TIMEOUT = (5, 30)
REQUEST_RETRIES = 3
REQUEST_INTERVAL = 1.0

RETRY_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}

# Historical data configuration
HISTORICAL_YEARS = 5


# Ensure required directories exist
for directory in (
    DATABASE_DIR,
    EXPORT_DIR,
    LOG_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
