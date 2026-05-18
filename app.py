from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        resume = data.get("resume")
        prompt = f"""
        You are a professional resume reviewer.
        Analyze this resume.
        Give:
        1. ATS Score out of 100
        2. Strengths
        3. Weaknesses
        4. Improvements
        5. Suggested Skills
        Resume:
        {resume}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        result = response.choices[0].message.content
        return jsonify({
            "result": result
        })
    except Exception as e:
        return jsonify({
            "result": str(e)
        })
if __name__ == "__main__":
    app.run(debug=True)