from flask import Flask, request, render_template
import requests
import os
import discogs_client

app = Flask(__name__)

user_token = os.environ.get("USER_TOKEN")
print(user_token)

d = discogs_client.Client('ExampleApplication/0.1', user_token=user_token)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Make a request to the API using the user's input
        results = d.search(user_input, type='release')
        #for release in results:
        #    return release.title
        return render_template('results.html', results=results)
    return render_template('index.html')