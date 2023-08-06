class PersistentVolumeClaimVolumeSource:
    def __init__(self, claim_name: str = None,
                 read_only: bool = None):
        self.claim_name = claim_name
        self.read_only = read_only
