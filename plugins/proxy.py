"""Opt-in HTTP transport routed through an explicit proxy."""

import base64
from urllib.parse import urljoin, urlparse

import requests

app_exfiltrate = None
config = None


def send(data):
    if not config.get('enabled', False):
        raise RuntimeError('proxy transport is disabled in configuration')
    url = urljoin(config['target'].rstrip('/') + '/',
                  config.get('path', '/collect').lstrip('/'))
    allowed = config.get('allowed_hosts', ['localhost', '127.0.0.1'])
    if urlparse(url).hostname not in allowed:
        raise ValueError('proxy target is not in allowed_hosts')
    payload = data.encode('utf-8') if isinstance(data, str) else data
    encoded = base64.b64encode(payload).decode('ascii')
    headers = dict(config.get('headers', {}))
    headers.setdefault('X-DET-Lab', '1')
    app_exfiltrate.log_message('info', '[proxy] Sending {} bytes via proxy'.format(len(payload)))
    requests.post(url, data=encoded, headers=headers,
                  proxies=config['proxies'], timeout=config.get('timeout', 10))


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('proxy', {'send': send})
