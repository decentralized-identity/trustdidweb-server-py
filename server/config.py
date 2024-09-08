from pydantic_settings import BaseSettings
import os
import uuid
import secrets
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "aries-did-web-server"
    PROJECT_VERSION: str = "v0"

    DOMAIN: str = os.environ["DOMAIN"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    DID_WEB_BASE: str = f"did:web:{DOMAIN}"
    ENDORSER_MULTIKEY: str = os.environ["ENDORSER_MULTIKEY"]
    ASKAR_DB: str = (
        os.environ["POSTGRES_URI"]
        if "POSTGRES_URI" in os.environ
        else "sqlite://app.db"
    )
    SCID_PLACEHOLDER: str = '{SCID}'


settings = Settings()
