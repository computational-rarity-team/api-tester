from flask import Flask, request, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import requests
import os, sys
import discogs_client

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

user_token = os.environ.get("USER_TOKEN")

d = discogs_client.Client('ExampleApplication/0.1', user_token=user_token)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        catnum = request.form['catnum']
        artist = request.form['artist']
        title = request.form['title']
        label = request.form['label']
        media = request.form['format']
        rating = request.form['rating']
        release = request.form['release']
        release_id = request.form['release_id']

        # Make a request to the API using the user's input
        results = d.search(title, release=release, artist=artist, label=label, format=media, catno=catnum, rating=rating)
        #for release in results:
        #    return release.title
        return render_template('results.html', results=results)
    return render_template('index.html')

# URL Routing - Flat Pages
# Retrieves the page path and
@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    return render_template(page)

@freezer.register_generator
def page():
    yield {'path': 'index.html'}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run()