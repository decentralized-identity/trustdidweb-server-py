import requests
import json
from app.plugins.agent import AgentController
from flask import current_app, session


class TDWService:
    def __init__(self):
        self.endpoint = current_app.config['TDW_SERVER_URL']
        self.endorser_multikey = current_app.config['TDW_ENDORSER_MULTIKEY']
        
    def register_did(self, name, scope):
        session['steps'] = []
        namespace = scope.replace(" ", "-").lower()
        identifier = name.replace(" ", "-").lower()
        r = requests.get(f'{self.endpoint}?namespace={namespace}&identifier={identifier}')
        did_request = r.json()
        
        session['steps'].append(
            {
                'index': '0',
                'title': 'Request identifier',
                'url': f'GET {self.endpoint}?namespace={namespace}&identifier={identifier}',
                'response': json.dumps(did_request, indent=2),
            }
        )
        
        did_document = did_request['didDocument']
        
        did = did_document['id']
        multikey_kid = f'{did}#multikey-01'
        multikey = AgentController().create_key(multikey_kid)
        
        did_document['@context'].append('https://w3id.org/security/multikey/v1')
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
        
        r = requests.post(f'{self.endpoint}/{namespace}/{identifier}', json={"didDocument": endorsed_did_document})
        
        session['steps'].append(
            {
                'index': '1',
                'title': 'Register identifier',
                'url': f'POST {self.endpoint}/{namespace}/{identifier}',
                'request': json.dumps({"didDocument": endorsed_did_document}, indent=2),
                'response': json.dumps(r.json(), indent=2),
            }
        )