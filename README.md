# Data Exfiltration Toolkit (DET) — Python 3 Port

A Python 3 port of SensePost’s Data Exfiltration Toolkit, prepared for a university cyber forensics project. The upstream version was written for Python 2 and used outdated dependencies. This port updates the code and dependencies for Python 3.

## Purpose

DET was developed as a proof of concept for evaluating data loss prevention (DLP) controls. Our class project used it to study file recovery and compare endpoint evidence with what an analyst can observe in Wireshark.

## Compatibility

| Component | Status |
| --- | --- |
| Python 3 | Port used for the classroom project |
| HTTP plugin | Worked in the local classroom lab. The recovered file matched the original byte for byte. |
| Core transports | Python 3 byte, base64, MIME, and hex conversions are ported |
| New lab transports | HTTPS, DNS TXT, WebSocket, S3-compatible storage, database, and proxy plugins are included; live compatibility is environment-dependent and unverified |

## Transport plugins

The repository includes the original transports (`http`, `dns`, `gmail`,
`google_docs`, `icmp`, `slack`, `tcp`, `twitter`, and `udp`) plus these
additional lab-oriented transports:

| Plugin | Intended lab use | External service or dependency |
| --- | --- | --- |
| `https` | HTTPS POSTs with headers, paths, user agents, and chunking | `requests` |
| `dns_txt` | DNS TXT queries carrying encoded test data | `dnslib` |
| `websocket` | Long-lived WebSocket sessions | `websocket-client` |
| `cloud_storage` | Uploads to S3-compatible storage such as MinIO | `boto3` |
| `database` | Inserts into an authorized PostgreSQL or MySQL lab database | `psycopg2-binary` or `mysql-connector-python` |
| `proxy` | HTTP requests routed through an explicit proxy | `requests` |

The new transports are disabled by default in `config-sample.json` and
`config-demo.json`. To use one, configure its local lab endpoint, confirm the
`allowed_hosts` or equivalent destination settings, and set its `enabled` value
to `true`. Database users must also create the configured destination table
before sending test data. Do not enable a transport against a service you do
not own or have explicit permission to test.

Install dependencies with:

    python3 -m pip install -r requirements.txt

## Repository layout

| Path | Purpose |
| --- | --- |
| `det.py` | Main Python 3 application |
| `plugins/` | Transport plugins |
| `requirements.txt` | Python dependencies |
| `config-sample.json` | Configuration reference with all transport fields |
| `config-demo.json` | Local demonstration configuration template |

Keep local configurations, credentials, captured traffic, and recovered files out of version control.

## Reviewing lab evidence

Open a saved capture from your authorized lab in Wireshark. Identify the endpoints, apply a display filter for the observed protocol, and inspect a relevant frame. Record what you can see, such as timestamps, packet lengths, and protocol headers. Label any separate plaintext comparison capture so readers can identify its source.

To verify recovery on Linux, set `original_file` and `recovered_file` to the paths of the two files, then run:

    sha256sum -- "$original_file" "$recovered_file"
    cmp -- "$original_file" "$recovered_file"

Matching SHA-256 hashes support the recovery finding. `cmp` exits with status `0` when both files contain exactly the same bytes.

## Credits and license

Original project by [SensePost](https://github.com/sensepost/DET). Copyright (c) 2016 SensePost. The upstream project is licensed under the MIT License. See `LICENSE` for the full text.

## Responsible use

Use this project only for education, defensive research, or security testing on systems and networks you own or have explicit permission to test. Do not use it for malicious purposes or unauthorized data transfers. Use non-sensitive test files in classroom labs.
