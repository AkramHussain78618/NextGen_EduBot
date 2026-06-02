from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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
            "srlimit": 1
        }

        response = requests.get(
            search_url,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        data = response.json()

        results = data.get("query", {}).get("search", [])

        if not results:
            return "Sorry, I could not find information."

        title = results[0]["title"]

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        summary_response = requests.get(
            summary_url,
            headers=HEADERS,
            timeout=10
        )

        if summary_response.status_code != 200:
            return "Sorry, I could not fetch information."

        summary_data = summary_response.json()

        extract = summary_data.get("extract", "")

        if not extract:
            return "Sorry, no summary available."

        return extract

    except Exception as e:
        print("ERROR:", e)
        return "Something went wrong while fetching answer."


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

    answer = fetch_wikipedia_content(question)

    return jsonify({
        "question": question,
        "answer": answer
    })


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
