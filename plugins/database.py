"""Opt-in database transport for an authorized PostgreSQL/MySQL lab database."""

import base64
import uuid

app_exfiltrate = None
config = None


def _connect():
    engine = config.get('engine', 'postgresql')
    if engine == 'postgresql':
        import psycopg2
        return psycopg2.connect(config['dsn'])
    if engine == 'mysql':
        import mysql.connector
        return mysql.connector.connect(**config['connection'])
    raise ValueError('database engine must be postgresql or mysql')


def send(data):
    if not config.get('enabled', False):
        raise RuntimeError('database transport is disabled in configuration')
    payload = data.encode('utf-8') if isinstance(data, str) else data
    encoded = base64.b64encode(payload).decode('ascii')
    table = config.get('table', 'det_lab_packets')
    if not table.replace('_', '').isalnum():
        raise ValueError('invalid database table name')
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO {} (packet_id, payload) VALUES (%s, %s)'.format(table),
            (str(uuid.uuid4()), encoded))
        connection.commit()
        app_exfiltrate.log_message(
            'info', '[database] Stored {} bytes in {}'.format(len(payload), table))
    finally:
        cursor.close()
        connection.close()


class Plugin:
    def __init__(self, app, conf):
        global app_exfiltrate, config
        app_exfiltrate, config = app, conf
        if conf.get('enabled', False):
            app.register_plugin('database', {'send': send})
