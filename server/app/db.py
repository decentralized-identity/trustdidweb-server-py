import json
from fastapi import HTTPException
from aries_askar import Store, error
from config import settings
import time
import uuid
import hashlib


class AskarStorage:
    def __init__(self):
        self.db = "sqlite://app.db"
        self.key = Store.generate_raw_key(
            hashlib.md5(settings.DID_WEB_BASE.encode()).hexdigest()
        )

    async def provision(self):
        await Store.provision(self.db, "raw", self.key, recreate=False)

    async def open(self):
        return await Store.open(self.db, "raw", self.key)

    async def fetch(self, category, data_key):
        store = await self.open()
        try:
            async with store.session() as session:
                data = await session.fetch(category, data_key)
            return json.loads(data.value)
        except:
            return None

    async def store(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.insert(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            raise HTTPException(status_code=404, detail="Could not store record")

    async def update(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.replace(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            raise HTTPException(status_code=404, detail="Could not update record")
