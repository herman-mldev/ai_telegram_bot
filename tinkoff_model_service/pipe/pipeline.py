from transformers import AutoTokenizer, AutoModelForCausalLM



class Pipeline:
    def __init__(self, tokenizer, model):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.model = AutoModelForCausalLM.from_pretrained(model)


    def cleanGeneratedResponses(self, generated_responses):
        replacements = [("@@ВТОРОЙ@@", " "), ("@@ПЕРВЫЙ@@", " ")]
        cleanedResponses = generated_responses.copy()
        
        for i, response in enumerate(cleanedResponses):
            for old, new in replacements:
                cleanedResponses[i] = cleanedResponses[i].replace(old, new)
            
            cleanedResponses[i] = cleanedResponses[i].strip()
        
        return cleanedResponses


    def generateResponse(self, message):
        encodedInputs = self.tokenizer(message, return_tensors="pt")
        input_ids = encodedInputs.input_ids

        generatedTokenIDs = self.model.generate(
            input_ids,
            top_k=10,
            top_p=0.95,
            num_beams=3,
            num_return_sequences=3,
            do_sample=True,
            no_repeat_ngram_size=2,
            temperature=1.2,
            repetition_penalty=1.2,
            length_penalty=1.0,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=40
        )

        contextWithResponse = [
            self.tokenizer.decode(sample_token_ids, skip_special_tokens=True)
            for sample_token_ids in generatedTokenIDs
        ]

        cleanedResponses = self.cleanGeneratedResponses(contextWithResponse)

        return cleanedResponses
        