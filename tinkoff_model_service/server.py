from quart import Quart, request, jsonify
from pipe.pipeline import Pipeline 
from tools.collector import Collector
from classifier.trainClassifier import Classifier
from classifier.trainModel import TrainModel



app = Quart(__name__)
pipelineInstance = Pipeline("tinkoff-ai/ruDialoGPT-medium", "tinkoff-ai/ruDialoGPT-medium")
requestsCollectorInstance = Collector("../data/telegram.json")
classifierInstance = Classifier("tinkoff-ai/ruDialoGPT-medium", "tinkoff-ai/ruDialoGPT-medium")
trainModelInstance = TrainModel("../data/telegram.json", "tinkoff-ai/ruDialoGPT-medium", "tinkoff-ai/ruDialoGPT-medium")


@app.route("/delivery", methods=["POST"])
async def delivery():
    data = await request.json
    message = data.get("message")

    print(f"Message received from the User: - {message}")

    response = pipelineInstance.generateResponse(message)
    requestsCollectorInstance.collectRequestAndResponse(message, response)
    bestResponse = classifierInstance.tokenizeAndPredict(message, response)

    response_data = {
        "response": bestResponse
    }

    return jsonify(response_data)


@app.route("/train", methods=["GET"])
async def train_model():
    try:
        trainModelInstance.train()
        return jsonify({"message": "Training completed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

