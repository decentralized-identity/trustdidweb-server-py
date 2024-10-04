from config import settings
from datetime import datetime, timezone
import canonicaljson
import json
from multiformats import multihash, multibase


class TrustDidWeb:
    def __init__(self):
        self.did_string_base = r'did:tdw:{SCID}:'+settings.DOMAIN
    
    def _define_parameters(self, update_key=None, next_key=None, ttl=100):
        # https://identity.foundation/trustdidweb/#generate-scid
        parameters = {
            "method": 'did:tdw:0.3',
            "scid": r"{SCID}",
            "updateKeys": [update_key],
            "portable": False,
            "prerotation": False,
            "nextKeyHashes": [],
            # "witness": {},
            "deactivated": False,
            "ttl": ttl,
        }
        return parameters
    
    def _generate_entry_hash(self, log_entry):
        # https://identity.foundation/trustdidweb/#generate-entry-hash
        jcs = canonicaljson.encode_canonical_json(log_entry)
        multihashed = multihash.digest(jcs, 'sha2-256')
        encoded = multibase.encode(multihashed, 'base58btc')[1:]
        return encoded
    
    def _generate_scid(self, log_entry):
        # https://identity.foundation/trustdidweb/#generate-scid
        jcs = canonicaljson.encode_canonical_json(log_entry)
        multihashed = multihash.digest(jcs, 'sha2-256')
        encoded = multibase.encode(multihashed, 'base58btc')[1:]
        return encoded
    
    def _add_placeholder_scid(self, item):
        if isinstance(item, str):
            return item.replace('did:web:', r'did:tdw:{SCID}:')
        elif isinstance(item, list):
            item['id'].replace('did:web:', r'did:tdw:{SCID}:')
            return item
        else:
            pass
    
    def _web_to_tdw(self, did_doc):
        did_doc['id'] = self._add_placeholder_scid(did_doc['id'])
        for idx, item in enumerate(did_doc['verificationMethod']):
            did_doc['verificationMethod'][idx] = self._add_placeholder_scid(did_doc['verificationMethod'][idx])
    
    def _init_parameters(self, update_key):
        return {
            "method": 'did:tdw:0.3',
            "scid": r"{SCID}",
            "updateKeys": [update_key],
            "portable": False,
            "prerotation": False,
            "nextKeyHashes": [],
            "deactivated": False,
        }
    
    def _init_did_doc(self):
        return {
            "@context": [],
            "id": r"{SCID}",
        }
        
    def provision_log_entry(self, did_doc, update_key):
        did_doc = json.loads(json.dumps(did_doc).replace('did:web:', r'did:tdw:{SCID}:'))
        preliminary_did_log_entry = [
            r'{SCID}', 
            str(datetime.now(timezone.utc).isoformat("T", "seconds")), 
            self._init_parameters(update_key=update_key),
            {
                "value": did_doc
            }
        ]
        scid = self._generate_scid(preliminary_did_log_entry)
        log_entry = json.loads(json.dumps(preliminary_did_log_entry).replace('{SCID}', scid))
        entry_hash = self._generate_entry_hash(log_entry)
        log_entry[0] = f'1-{entry_hash}'
        return log_entry
    
    def create(self, did_doc):
        # https://identity.foundation/trustdidweb/#create-register
        did_string = did_doc['id'].replace('did:web:', r'did:tdw:{SCID}:')
        authorized_keys = []
        initial_did_doc = self._web_to_tdw(did_doc)
        parameters = self._define_parameters(update_key=did_doc['verificaitonMethod'][0]['publicKeyMultibase'])
        did_log_entry = [
            r'{SCID}', 
            str(datetime.now().isoformat('T', 'seconds')), 
            parameters,
            {"value": initial_did_doc}
        ]
        scid = self._generate_scid(did_log_entry)
        did_log_entry = json.loads(json.dumps(did_log_entry).replace('{SCID}', scid))
        log_entry_hash = self._generate_entry_hash(did_log_entry)
        did_log_entry[0] = f'1-{log_entry_hash}'