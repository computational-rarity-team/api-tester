from flask import Flask, request, render_template
from flask_frozen import Freezer
import os, sys
import discogs_client

app = Flask(__name__)
app.config.from_object(__name__)

app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

user_token = os.environ.get("USER_TOKEN")

d = discogs_client.Client('ExampleApplication/0.1', user_token=user_token)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results")
def results():
    catnum = request.args.get('catnum')
    artist = request.args.get('artist')
    title = request.args.get('title')
    label = request.args.get('label')
    media = request.args.get('format')
    rating = request.args.get('rating')
    release = request.args.get('release')
    release_id = request.args.get('release_id')

    # Make a request to the API using the user's input
    results = d.search(title, release=release, artist=artist, label=label, format=media, catno=catnum, rating=rating)
    
    return render_template('results.html', results=results)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.run(debug=True)
    else:
        app.run()