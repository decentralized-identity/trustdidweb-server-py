from pydantic_settings import BaseSettings
import os
import uuid
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "aries-did-web"
    PROJECT_VERSION: str = "v0"

    CHALLENGE_SALT: uuid.UUID = uuid.uuid4()
    DOMAIN: str = os.environ["DOMAIN"]
    DID_WEB_BASE: str = 'did:web:'+DOMAIN
    DID_TDW_BASE: str = r'did:web:{{SCID}}:'+DOMAIN
    WITNESS_MULTIKEY: str = os.environ["WITNESS_MULTIKEY"]


settings = Settings()
