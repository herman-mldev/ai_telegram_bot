import os
import torch
import json
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM



class TrainModel:
    def __init__(self, dataset, tokenizer, model):
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        self.dataset = os.path.join(scriptDirectory, dataset)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.model = AutoModelForCausalLM.from_pretrained(model)
        self.criterion = nn.MSELoss()
    

    def updateModel(self, user_question, generated_response, optimizer):
        usersRequestTokenized = self.tokenizer(user_question, padding=True, truncation=True, return_tensors="pt")
        generatedResponseTokenized = self.tokenizer(generated_response, padding=True, truncation=True, return_tensors="pt")
        
        optimizer.zero_grad()
        outputs = self.model(**usersRequestTokenized, labels=generatedResponseTokenized["input_ids"])
        loss = outputs.loss
        loss.backward()
        optimizer.step()


    def train(self):
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        with open(self.dataset, "r") as f:
            data = json.load(f)

        examples = data["users_requests"]
        messages = data["messages"]

        for userRequest, generatedResponses, correctResponse in zip(examples, messages):
            losses = []
            for response in generatedResponses:
                _, mse_loss, predicted_label = self.tokenizeAndPredict(userRequest, response)
                losses.append(mse_loss)

            bestResponseIndex = losses.index(min(losses))
            bestResponse = generatedResponses[bestResponseIndex]

            print(f"User Question: {userRequest}")
            print(f"Correct Response: {correctResponse}")
            print(f"Best Response: {bestResponse}")
            print(f"Predicted Label: {predicted_label}")
            print("--------------------")

            self.updateModel(userRequest, bestResponse, optimizer)