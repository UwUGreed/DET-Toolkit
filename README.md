# Data Exfiltration Toolkit (DET) — Python 3 Port

A Python 3 port of SensePost’s Data Exfiltration Toolkit, prepared for a university cyber forensics project. The upstream version was written for Python 2 and used outdated dependencies. This port updates the code and dependencies for Python 3.

## Purpose

DET was developed as a proof of concept for evaluating data loss prevention (DLP) controls. Our class project used it to study file recovery and compare endpoint evidence with what an analyst can observe in Wireshark.

## Compatibility

| Component | Status |
| --- | --- |
| Python 3 | Port used for the classroom project |
| HTTP plugin | Worked in the local classroom lab. The recovered file matched the original byte for byte. |
| Other plugins | Included from upstream. End-to-end compatibility is unverified. |

## Repository layout

| Path | Purpose |
| --- | --- |
| `det.py` | Main Python 3 application |
| `plugins/` | Transport plugins |
| `requirements.txt` | Python dependencies |
| `config-sample.json` | Upstream configuration reference |

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
