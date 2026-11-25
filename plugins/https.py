"""Opt-in HTTPS POST transport for controlled lab endpoints."""

import base64
from urllib.parse import urljoin, urlparse

import requests

app_exfiltrate = None
config = None


def _check_target(url):
    if not config.get('enabled', False):
        raise RuntimeError('https transport is disabled in configuration')
    host = urlparse(url).hostname
    allowed = config.get('allowed_hosts', ['localhost', '127.0.0.1'])
    if host not in allowed:
        raise ValueError('HTTPS target is not in allowed_hosts')


def send(data):
    path = config.get('path', '/collect')
    url = urljoin(config['target'].rstrip('/') + '/', path.lstrip('/'))
    _check_target(url)
    payload = data.encode('utf-8') if isinstance(data, str) else data
    encoded = base64.b64encode(payload).decode('ascii')
    chunk_size = int(config.get('chunk_size', len(encoded)))
    headers = dict(config.get('headers', {}))
    headers.setdefault('X-DET-Lab', '1')
    headers.setdefault('User-Agent', config.get('user_agent', 'DET-Lab/1.0'))
    for offset in range(0, len(encoded), chunk_size):
        chunk = encoded[offset:offset + chunk_size]
        app_exfiltrate.log_message(
            'info', '[https] Sending {} bytes to {}'.format(len(chunk), url))
        requests.post(url, data=chunk, headers=headers,
                      timeout=config.get('timeout', 10),
                      proxies=config.get('proxies'))


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('https', {'send': send})
