from flask import Flask, request, redirect, render_template, url_for
from flask.views import MethodView

import os
import urllib3
import discogs_client


app = Flask(__name__)
user_token = os.environ.get("USER_TOKEN")
http = urllib3.PoolManager()
r = http.request('GET', 'https://musicbrainz.org/ws/2/') # grab music information from musicbrainz


d = discogs_client.Client('ExampleApplication/0.1', user_token=user_token)

# @app.route("/")
# def find_result():
#     results = d.search('SHAKER LOOPS', type='release')

    # for release in results:
    #     return release.title

class MusicApiView(MethodView):
    def get(self):
        print(request)
        content = {}
        return render_template("index.html", content=content)

    def post(self):
        data = request.form.get("title")
        music_type = ""
        results = d.search(data, type='release')
        print(type(results))
        return render_template("index.html", content=results)
        # return redirect(url_for("/music/"))



app.add_url_rule('/music/', view_func=MusicApiView.as_view('/music/'))
@app.route("/")
def index():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
    