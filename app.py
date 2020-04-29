import environ
from flask import Flask, request, redirect
import requests
import re

application = Flask(__name__)

env = environ.Env()
application.config["SRC_DOMAIN"] = env('SRC_DOMAIN')
application.config["DEST_DOMAIN"] = env('DEST_DOMAIN')

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def main(path):
    url = re.sub(application.config["SRC_DOMAIN"], application.config["DEST_DOMAIN"], request.url)
    return redirect(url, code=301)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
