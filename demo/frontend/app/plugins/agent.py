import requests




class AgentController:
    def __init__(self):
        self.endpoint = ''
        
    def create_key(self, kid):
        r = requests.post(f'{self.endpoint}/wallet/keys', json={
            'kid': kid
        })
        return r.json(['multikey'])
        
    def add_proof(self, document, options):
        r = requests.post(f'{self.endpoint}/vc/di/add-proof', json={
            'document': document,
            'options': options,
        })
        return r.json(['securedDocument'])