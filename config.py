import os
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
update_channel = os.getenv("update_channel")
tru_bot =os.getenv("BOT_USER")
OWNER_ID = list({int(x) for x in os.environ.get("OWNER_ID", "").split()})
