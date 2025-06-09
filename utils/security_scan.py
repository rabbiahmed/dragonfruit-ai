# utils/security_scan.py
'''
This function doesn't currently handle DNS or socket errors like gaierror which occurs when an invalid hostname or IP
(256.256.256.256) is used.
'''

import socket


def simple_port_scan(host="127.0.0.1", ports=None):
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 993, 995, 3389, 8080, 8443]  # Common ports
        # FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, IMAP, HTTPS, SMB, IMAP over SSL, POP3over SSL, RDP, Alternative HTTPs

    results = []
    try:
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                try:
                    s.connect((host, port))
                    results.append((port, True))
                except (socket.timeout, ConnectionRefusedError):
                    results.append((port, False))
    except socket.gaierror:
        # Hostname could not be resolved
        return [("error", "Invalid host")]
    except Exception as e:
        return [("error", str(e))]

    return results
