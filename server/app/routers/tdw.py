from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.web_requests import RegisterDID
from config import settings
from app.plugins import AskarVerifier, AskarStorage, TrustDidWeb
from app.dependencies import (
    identifier_available,
    did_document_exists,
    valid_did_registration,
)
from app.utilities import create_did_doc_template

router = APIRouter()