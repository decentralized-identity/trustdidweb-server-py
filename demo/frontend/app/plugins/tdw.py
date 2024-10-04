import requests
from app.plugins.agent import AgentController


class TDWService:
    def __init__(self):
        self.endpoint = ''
        self.endorser_multikey = ''
        
    def register_did(self, namespace, identifier):
        did_request = self.request_did(namespace, identifier)
        
        did_document = did_request['didDocument']
        
        did = did_document['id']
        multikey_kid = f'{did}#multikey-01'
        multikey = AgentController().create_key(multikey_kid)
        
        did_document['context'] += 'https://w3id.org/security/multikey/v1'
        did_document['authentication'] = [multikey_kid]
        did_document['assertionMethod'] = [multikey_kid]
        did_document['verificationMethod'] = [{
            'id': multikey_kid,
            'type': 'Multikey',
            'controller': did,
            'publicKeyMultibase': multikey,
        }]
        
        proof_options = did_request['proofOptions']
        
        client_proof_options = proof_options.copy()
        client_proof_options['verificationMethod'] = f'did:key:{multikey}#{multikey}'
        signed_did_document = AgentController().add_proof(did_document, client_proof_options)
        
        endorser_proof_options = proof_options.copy()
        endorser_proof_options['verificationMethod'] = f'did:key:{self.endorser_multikey}#{self.endorser_multikey}'
        endorsed_did_document = AgentController().add_proof(signed_did_document, endorser_proof_options)
        did_document = self.register_did(endorsed_did_document)
        return did_document
        
    def request_did(self, namespace, identifier):
        r = requests.get(f'{self.endpoint}?namespace={namespace}&identifier={identifier}')
        return r.json()
        
    def register_did(self, endorsed_did_document):
        did = endorsed_did_document['id']
        namespace = did.split(':')[-2]
        identifier = did.split(':')[-1]
        r = requests.get(f'{self.endpoint}/{namespace}/{identifier}', json=endorsed_did_document)
        return r.json()['didDocument']