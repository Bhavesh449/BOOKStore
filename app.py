from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """
You are Shiva AI, an exam-topper AI assistant for Class 9 and Class 10 students.

Rules:
- Answer like a board-exam topper.
- Explain step-by-step.
- Use simple English or Hinglish.
- SST answers MUST be in points.
- Focus on definitions, points, formulas, and examples.
- If asked numericals, solve clearly with steps.
- Be motivating and student-friendly.
"""

# Load knowledge file
KNOWLEDGE_FILE = "knowledge.txt"
def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read().lower()
    return ""
KNOWLEDGE_BASE = load_knowledge()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    raw_msg = request.json.get("message", "").strip()
    user_msg = raw_msg.lower()

    # ✅ Greeting intent
    greetings = ["hi", "hello", "hey", "hii", "hiii"]
    if user_msg in greetings and len(user_msg.split()) <= 2:
        return jsonify({
            "reply": "Hey, I am Shiva, an AI founded by Bhavesh for helping Class 10 Boards students. Ask me anything 😊📚"
        })

    # ✅ Check knowledge file first
    if any(keyword in KNOWLEDGE_BASE for keyword in user_msg.split()):
        # Find matching line(s)
        lines = [line for line in KNOWLEDGE_BASE.split("\n") if all(word in line for word in user_msg.split())]
        if lines:
            answer = " ".join(lines)
            formatted_answer = f"💡 According to my knowledge:\n{answer}"
            return jsonify({"reply": formatted_answer})

    # ✅ Keywords related to Bhavesh / Admin / Owner
    bhavesh_keywords = ["admin", "owner", "owned by", "who is bhavesh", "bhavesh", "founder", "creator"]
    if any(keyword in user_msg for keyword in bhavesh_keywords):
        return jsonify({
            "reply": "Bhavesh is the Admin of BOOKStore and Founder of Edupie, helping Class 10 students score higher marks in Boards 😊"
        })

    # ✅ Other known people
    people = {
        "rishi": "Rishi is the Class 10th English Topper and Friend of Admin 😊",
        "mayank": "Mayank is the Class 9th Topper and Best Friend of Admin 😊",
        "rehan": "Rehan is the Best Friend of Admin 😊",
        "saina": "Saina is the Bestiest Friend of Admin 😊"
    }

    for name, reply in people.items():
        if name in user_msg:
            return jsonify({"reply": reply})

    # ✅ Default AI response if not in knowledge base
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_msg}
            ],
            temperature=0.3
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("AI Error:", e)
        return jsonify({
            "reply": "⚠️ Shiva is facing a small issue. Please try again."
        })


if __name__ == "__main__":
    app.run(debug=True)
