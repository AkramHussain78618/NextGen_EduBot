from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "StudentChatbot/1.0"
}

def get_answer(question):

    try:

        # Wikipedia Search API
        search_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": question,
            "format": "json"
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
            return "No information found."

        title = results[0]["title"]

        # Get summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        summary_response = requests.get(
            summary_url,
            headers=HEADERS,
            timeout=10
        )

        summary_data = summary_response.json()

        answer = summary_data.get("extract")

        if not answer:
            return "No summary available."

        return answer

    except Exception as e:
        print("ERROR:", e)
        return "Something went wrong while fetching information."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("message", "")

    answer = get_answer(question)

    if len(answer) > 700:
        answer = answer[:700] + "..."

    return jsonify({
        "question": question,
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)