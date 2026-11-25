"""Opt-in S3-compatible object upload transport (for example, local MinIO)."""

import base64
import io
import uuid

app_exfiltrate = None
config = None


def send(data):
    if not config.get('enabled', False):
        raise RuntimeError('cloud_storage transport is disabled in configuration')
    import boto3

    payload = data.encode('utf-8') if isinstance(data, str) else data
    object_key = '{}-{}.b64'.format(config.get('prefix', 'det-lab'), uuid.uuid4())
    encoded = base64.b64encode(payload)
    client = boto3.client(
        's3', endpoint_url=config['endpoint_url'],
        region_name=config.get('region', 'us-east-1'),
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'])
    app_exfiltrate.log_message(
        'info', '[cloud_storage] Uploading {} bytes as {}'.format(
            len(payload), object_key))
    client.upload_fileobj(io.BytesIO(encoded), config['bucket'], object_key,
                          ExtraArgs={'ContentType': 'text/plain',
                                     'Metadata': {'det-lab': '1'}})


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('cloud_storage', {'send': send})
