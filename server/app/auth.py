from fastapi import HTTPException
from config import settings
import uuid
import canonicaljson
import nacl
from hashlib import sha256
from app import multibase


def did_auth():
    pass

def verify_assertion_proof(did_doc, proof):
    # try:
    assert proof['type'] == 'DataIntegrityProof'
    assert proof['cryptosuite'] == 'eddsa-jcs-2022'
    assert proof['proofPurpose'] == 'assertionMethod'
    assert proof["domain"] == settings.DID_WEB_BASE.split(":")[-1]
    # assert proof["challenge"] == str(
    #     uuid.uuid5(settings.CHALLENGE_SALT, proof["created"])
    # )
    assert proof['verificationMethod'].split('#')[0] == did_doc['id']
    verification_method = next(
            (vm for vm in did_doc['verificationMethod'] if vm["id"] == proof['verificationMethod']),
            None,
        )
                
    proof_options = proof.copy()
    proof_value = proof_options.pop('proofValue')
    proof_bytes = multibase.decode(proof_value)
            
    hash_data = (
        sha256(canonicaljson.encode_canonical_json(did_doc)).digest()+
        sha256(canonicaljson.encode_canonical_json(proof_options)).digest()
    )
    if verification_method['type'] == 'MultiKey':
        pub_key = multibase.decode(verification_method['publicKeyMultibase'])
        public_key_bytes = bytes(bytearray(pub_key)[2:])
    # nacl.bindings.crypto_sign_open(proof_bytes + hash_data, public_key_bytes)
    # except nacl.exceptions.BadSignatureError:
    #     raise HTTPException(status_code=400, detail="Invalid assertionMethod proof.")

def verify_auth_proof(did_doc, proof):
    # try:
    assert proof['type'] == 'DataIntegrityProof'
    assert proof['cryptosuite'] == 'eddsa-jcs-2022'
    assert proof['proofPurpose'] == 'assertionMethod'
    assert proof["domain"] == settings.DID_WEB_BASE.split(":")[-1]
    # assert proof["challenge"] == str(
    #     uuid.uuid5(settings.CHALLENGE_SALT, proof["created"])
    # )
    assert proof['verificationMethod'].split('#')[0] == settings.DID_WEB_BASE
                
    proof_options = proof.copy()
    proof_value = proof_options.pop('proofValue')
    proof_bytes = multibase.decode(proof_value)
            
    hash_data = (
        sha256(canonicaljson.encode_canonical_json(did_doc)).digest()+
        sha256(canonicaljson.encode_canonical_json(proof_options)).digest()
    )

    pub_key = multibase.decode(settings.WITNESS_MULTIKEY)
    public_key_bytes = bytes(bytearray(pub_key)[2:])
    # nacl.bindings.crypto_sign_open(proof_bytes + hash_data, public_key_bytes)
    # except nacl.exceptions.BadSignatureError:
    #     raise HTTPException(status_code=400, detail="Invalid authentication proof.")