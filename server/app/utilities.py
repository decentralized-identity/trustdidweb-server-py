from app.models.did_document import DidDocument
from config import settings


def derive_did(namespace, identifier):
    return f"{settings.DID_WEB_BASE}:{namespace}:{identifier}"


def create_did_doc(did, multikey, kid="key-01"):
    return DidDocument(
        id=did,
        verificationMethod=[
            {
                "id": kid,
                "type": "Multikey",
                "controller": did,
                "publicKeyMultibase": multikey,
            }
        ],
        authentication=[kid],
        assertionMethod=[kid],
        service=[],
    ).model_dump()


def find_key(did_doc, kid):
    return next(
        (
            vm["publicKeyMultibase"]
            for vm in did_doc["verificationMethod"]
            if vm["id"] == kid
        ),
        None,
    )


def find_proof(proof_set, kid):
    return next(
        (proof for proof in proof_set if proof["verificationMethod"] == kid),
        None,
    )
