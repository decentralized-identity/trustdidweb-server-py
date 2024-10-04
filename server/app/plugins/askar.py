import json
from fastapi import HTTPException
from aries_askar import Store, Key
from aries_askar.bindings import LocalKeyHandle
from config import settings
import hashlib
import uuid
from multiformats import multibase
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import canonicaljson


class AskarStorage:
    def __init__(self):
        self.db = settings.ASKAR_DB
        self.key = Store.generate_raw_key(
            hashlib.md5(settings.DOMAIN.encode()).hexdigest()
        )

    async def provision(self, recreate=False):
        await Store.provision(self.db, "raw", self.key, recreate=recreate)

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
                await session.insert(category, data_key, json.dumps(data))
        except:
            raise HTTPException(status_code=404, detail="Couldn't store record.")

    async def update(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.replace(category, data_key, json.dumps(data))
        except:
            raise HTTPException(status_code=404, detail="Couldn't update record.")


class AskarVerifier:
    def __init__(self):
        self.type = "DataIntegrityProof"
        self.cryptosuite = "eddsa-jcs-2022"
        self.purpose = "authentication"

    def create_proof_config(self, did):
        expires = str(
            (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(
                "T", "seconds"
            )
        )
        return {
            "type": self.type,
            "cryptosuite": self.cryptosuite,
            "proofPurpose": self.purpose,
            "verificationMethod": f"did:key:{settings.ENDORSER_MULTIKEY}#{settings.ENDORSER_MULTIKEY}",
            "expires": expires,
            "domain": settings.DOMAIN,
            "challenge": self.create_challenge(did + expires),
        }

    def create_challenge(self, value):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, settings.SECRET_KEY + value))

    def assert_proof_options(self, proof, did):
        try:
            assert datetime.fromisoformat(proof["expires"]) > datetime.now(
                timezone.utc
            ), "Proof expired."
            assert proof["domain"] == settings.DOMAIN, "Domain mismatch."
            assert proof["challenge"] == self.create_challenge(
                did + proof["expires"]
            ), "Challenge mismatch."
            assert proof["type"] == self.type, f"Expected {self.type} proof type."
            assert (
                proof["cryptosuite"] == self.cryptosuite
            ), f"Expected {self.cryptosuite} proof cryptosuite."
            assert (
                proof["proofPurpose"] == self.purpose
            ), f"Expected {self.purpose} proof purpose."
        except AssertionError as msg:
            raise HTTPException(status_code=400, detail=str(msg))

    def verify_proof(self, document, proof):
        self.assert_proof_options(proof, document["id"])

        multikey = proof["verificationMethod"].split("#")[-1]

        key = Key(LocalKeyHandle()).from_public_bytes(
            alg="ed25519", public=bytes(bytearray(multibase.decode(multikey))[2:])
        )

        proof_options = proof.copy()
        signature = multibase.decode(proof_options.pop("proofValue"))

        hash_data = (
            sha256(canonicaljson.encode_canonical_json(proof_options)).digest()
            + sha256(canonicaljson.encode_canonical_json(document)).digest()
        )
        try:
            if not key.verify_signature(message=hash_data, signature=signature):
                raise HTTPException(
                    status_code=400, detail="Signature was forged or corrupt."
                )
        except:
            raise HTTPException(status_code=400, detail="Error verifying proof.")
