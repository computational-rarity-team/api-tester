from flask import Flask
from flask import render_template
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

#     for release in results:
#         return release.title

class MusicApiView(MethodView):
    def get(self):
        # print(*db.session.query(RegexModel).all())
        return render_template("index.html")

    def post(self):
        regex, text = request.form.get("regex"), request.form.get("text")
        pattern = re.compile(regex)
        result, post = bool(pattern.match(text)), True
        obj = RegexModel(regex=regex, text=text, result=result)
        db.session.add(obj)
        db.session.commit()


@app.route("/")
def index():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
    