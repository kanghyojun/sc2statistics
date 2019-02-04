from flask import url_for as web_url_for

from sc2web.web.app import app


def url_for(*args, **kwargs):
    with app.test_request_context():
        return web_url_for(*args, **kwargs)
