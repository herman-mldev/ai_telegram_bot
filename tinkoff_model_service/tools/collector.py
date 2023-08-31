import json
import os
from validation.requestValidation import RequestValidation
from validation.responseModelValidation import responseModelValidation


class Collector:
    def __init__(self, dataset):
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        self.dataset = os.path.join(scriptDirectory, dataset)
        self.data = self.loadDataset()

    def loadDataset(self):
        with open(self.dataset, "r") as f:
            return json.load(f)

    def saveDataset(self):
        with open(self.dataset, "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def collectRequestAndResponse(self, request_text, response_data):
        if (
            not RequestValidation(self.data).isDuplicateRequest(request_text) and
            not responseModelValidation(self.data).isDuplicateResponse(response_data)
        ):
            new_request = request_text
            new_data = response_data
            self.data["users_requests"].append(new_request)
            self.data["messages"].extend(new_data)
            self.saveDataset()
        else:
            print("Duplicate request or response. Not collecting.")
