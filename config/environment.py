from dotenv import load_dotenv
from config.settings import BASE_DIR

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)
