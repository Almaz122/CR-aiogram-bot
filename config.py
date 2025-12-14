import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Clash Royale API Token
CR_API_TOKEN = os.getenv("CR_API_TOKEN", "")

# Clash Royale API Base URL
CR_API_BASE_URL = "https://api.clashroyale.com/v1"

# Clan Tag (без #)
CLAN_TAG = os.getenv("CLAN_TAG", "")

