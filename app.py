from flask import Flask, request, redirect, render_template, url_for
from flask.views import MethodView
import os
import urllib3
import discogs_client
import musicbrainzngs as mz
import logging


app = Flask(__name__)
user_token = os.environ.get("USER_TOKEN")
user_email = os.environ.get("USER_EMAIL")
print(os.environ.get("USER_PASSWORD"), user_email)
# musivbrains config
mz.auth(os.environ.get("USER_NAME"),  os.environ.get("USER_PASSWORD")) # musicbrain authentication
mz.set_useragent(app="api-tester", version="0.0.1", contact=user_email)
mz.set_format(fmt='json') # sets the returned format to json

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
        d_results = d.search(data, type='release') # discogs results
        mzb_results = mz.search_artists(query=data, limit=5, offset=None, strict=False, sortname=True) # searching musicbrains database
        print(type(d_results), mzb_results)
        return render_template("index.html", content=mzb_results)
        # return redirect(url_for("/music/"))



app.add_url_rule('/music/', view_func=MusicApiView.as_view('/music/'))
@app.route("/")
def index():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
    