class TokenManager:
    def __init__(self):
        self.token = None

    def parseToken(self, filename: str) -> str:
        with open(filename, "r") as f:
            self.token = f.read().strip()
        
        return self.token