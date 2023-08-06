import downloader

from dotenv import load_dotenv

from flask import Flask, request
from werkzeug.exceptions import BadRequest

from super_eureka import logging

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/main/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        body: dict = request.get_json()
        download_link: str = body.get('download_link', '')
        if download_link:
            downloader.download_and_process(download_link)
            return 'The download process was initiated.'
    raise BadRequest


def serve() -> None:
    logging.initialize()
    load_dotenv()
    app.run(port=5500)


if __name__ == "__main__":
    serve()
