import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM



class Classifier:
    def __init__(self, tokenizer, model):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.model = AutoModelForCausalLM.from_pretrained(model)


    def tokenizeAndPredict(self, user_question, generated_response):
            userQuestionTokenized = self.tokenizer(user_question, padding=True, truncation=True, return_tensors="pt")
            generatedResponseTokenized = self.tokenizer(generated_response, padding=True, truncation=True, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**userQuestionTokenized)
                predictions = F.softmax(outputs.logits, dim=1)
                labels = torch.argmax(predictions, dim=1)
                print(labels)

            generatedResponseString = self.tokenizer.decode(
                generatedResponseTokenized["input_ids"][0][len(userQuestionTokenized["input_ids"][0]):],
                skip_special_tokens=True
            )

            return generatedResponseString
    