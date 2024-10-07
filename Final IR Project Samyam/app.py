from flask import Flask, render_template, request
from search_engine import StorySearchEngine

app = Flask(__name__)

# Initialize the search engine with the path to your dataset directory
search_engine = StorySearchEngine(r'./datasets', r'./utils/story_image.json')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_engine.search(query)
        return render_template("index.html", results=results)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
