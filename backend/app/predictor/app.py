from flask import Flask, request, jsonify
import pickle
from google.cloud import storage

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return "ok"


def download_model():
    print("Downloading model from GCS...")
    client = storage.Client()
    bucket = client.bucket("kenneth-vertex-bucket-mlops")
    blob = bucket.blob("model/policy.pkl")

    local_path = "/tmp/policy.pkl"
    blob.download_to_filename(local_path)

    print("Model downloaded successfully ✅")
    return local_path

MODEL_PATH = download_model()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

policy = model["policy"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    instances = data["instances"]

    predictions = []

    for inst in instances:
        state = tuple(inst)
        action = policy.get(state, 0)
        predictions.append(action)

    return jsonify({"predictions": predictions})

@app.route("/health", methods=["GET"])
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)