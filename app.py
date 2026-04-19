
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_ai_response(message):
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model":"llama-3.1-8b-instant",   # ✅ Working model
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
        )

        # 🔍 Debug (see terminal output)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        data = response.json()

        # ✅ Handle correct response
        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        # ❌ Handle API error
        elif "error" in data:
            return "API Error: " + data["error"]["message"]

        # ❓ Unknown response
        else:
            return "Unexpected response: " + str(data)

    except Exception as e:
        return "Error: " + str(e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not user_msg:
        return jsonify({"reply": "Please enter a message"})

    reply = get_ai_response(user_msg)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)