class responseModelValidation():
    def __init__(self, data):
        self.data = data

    def isDuplicateResponse(self, response_text):
        return response_text in self.data["messages"]
