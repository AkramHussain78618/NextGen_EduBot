from flask import Flask, render_template, request, jsonify
import requests
from transformers import pipeline

app = Flask(__name__)

# ✅ QA Model (fixed & correct)
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)
# ✅ Summarizer Model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

HEADERS = {
    "User-Agent": "NextGenEduBot/1.0"
}


# -----------------------------
# Wikipedia Fetch Function
# -----------------------------
def fetch_wikipedia_content(question):
    try:
        search_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": question,
            "format": "json",
            "utf8": 1,
            "srlimit": 3
        }

        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
        data = response.json()

        results = data.get("query", {}).get("search", [])

        if not results:
            return None

        for result in results:
            title = result["title"]

            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

            summary_response = requests.get(summary_url, headers=HEADERS, timeout=10)

            if summary_response.status_code != 200:
                continue

            summary_data = summary_response.json()
            extract = summary_data.get("extract", "")

            if "may refer to" in extract.lower() or len(extract) < 50:
                continue

            return extract

        return None

    except Exception as e:
        print("WIKIPEDIA ERROR:", e)
        return None


# -----------------------------
# AI Answer Generator
# -----------------------------
def generate_answer(question):
    try:
        content = fetch_wikipedia_content(question)

        if not content:
            return "Sorry, I could not find relevant information."

        context = content[:2000]

        result = qa_pipeline({
            "question": question,
            "context": context
        })

        answer = result.get("answer", "").strip()
        score = result.get("score", 0)

        # fallback to summarizer
        if score < 0.2 or len(answer) < 5:
            summary = summarizer(
                context,
                max_length=120,
                min_length=40,
                do_sample=False
            )
            return summary[0]["summary_text"]

        return answer

    except Exception as e:
        print("AI ERROR:", e)
        return "Something went wrong while generating answer."


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "")

    answer = generate_answer(question)

    return jsonify({
        "question": question,
        "answer": answer
    })


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)