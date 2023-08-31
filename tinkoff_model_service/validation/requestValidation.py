class RequestValidation:
    def __init__(self, data):
        self.data = data

    def isDuplicateRequest(self, request_text):
        return request_text in self.data["users_requests"]
