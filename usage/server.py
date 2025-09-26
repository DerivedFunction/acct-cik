from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = Flask(__name__)

# Paths
MODEL_PATH = "model"  # your saved Hugging Face model

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
print("Model loaded")
model.eval()  # evaluation mode

# Mapping IDs to labels
id2label = {
    0: "Confirmed hedging derivative usage",
    1: "Likely hedging derivative usage (not confirmed for reporting year)",
    2: "Mentions derivatives, speculative or policy-related",
    3: "Irrelevant / unrelated context",
    4: "Warrants and Derivative Liability",  # New Label
}
label2id = {v: k for k, v in id2label.items()}


# Prediction function for batches
def predict_batch(texts):
    # Tokenize the batch
    inputs = tokenizer(
        texts, padding=True, truncation=True, max_length=512, return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_ids = torch.argmax(logits, dim=1).tolist()

    # Map to label strings
    predictions = {"predictions": [{"label_id": pid, "label": id2label[pid]} for pid in predicted_ids]}
    
    # Write results to tab-separated file
    with open('predictions.xml', 'a') as f:
        for idx, (text, pred) in enumerate(zip(texts, predictions['predictions'])):
            case_string = f"<case num=\"{idx}\"><text>{text}</text><label>{pred['label']}</label><label_id>{pred['label_id']}</label_id></case>\n"
            f.write(case_string)
            
    return predictions


# Flask route
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json
    if "texts" not in data or not isinstance(data["texts"], list):
        return (
            jsonify({"error": "Missing or invalid 'texts' field; must be a list"}),
            400,
        )
    texts = data["texts"]
    predictions = predict_batch(texts)
    return jsonify(predictions)


# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
