import os, asyncio
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_path = os.getenv("TG_SESSION_PATH", "./.secrets/telethon.session")
Path(session_path).parent.mkdir(parents=True, exist_ok=True)

async def main():
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()  # спросит номер и код из Telegram
    me = await client.get_me()
    print("Authorized as:", getattr(me, "username", None) or me.id)
    await client.disconnect()

asyncio.run(main())