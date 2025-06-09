# utils/system_info.py

import socket
import logging
import time
import platform
from utils.network_type_detector import get_active_interfaces
from utils.wifi_security import check_wifi_security
from utils.vulnerability_assessor import detect_firewall

try:
    import distro  # Linux distro info (only available on Linux)
except ImportError:
    distro = None  # Safe fallback if 'distro' is not available


def check_internet_connectivity(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except (socket.timeout, OSError) as e:
        logging.warning(f"Internet connectivity check failed: {e}")
        return False


def detect_os():
    try:
        os_info = platform.system()
    except (OSError, ValueError) as e:
        return f"OS detection failed: {e}"

    if os_info == "Linux":
        if distro:
            try:
                name = distro.name(pretty=True)
                return name if name else "Linux (Unknown Distro)"
            except (AttributeError, RuntimeError) as e:
                return f"Linux (Distro detection failed: {e})"
        else:
            return "Linux (distro module not available)"
    elif os_info == "Darwin":
        try:
            version = platform.mac_ver()[0]
            return f"macOS {version}" if version else "macOS (Unknown version)"
        except (OSError, IndexError) as e:
            return f"macOS (Version detection failed: {e})"
    else:
        try:
            release = platform.release()
            return f"{os_info} {release}"
        except OSError as e:
            return f"{os_info} (Release detection failed: {e})"


def collect_system_summary(start_time=None):

    if start_time is not None:
        try:
            scan_time = round(time.time() - start_time, 2)
        except (TypeError, ValueError) as e:
            scan_time = f"Error calculating scan time: {e}"
    else:
        scan_time = "N/A"

    active_interfaces = get_active_interfaces()

    summary = {
        "internet": "Connected" if check_internet_connectivity() else "Disconnected",
        "connection_type": ", ".join(active_interfaces) or "No active interfaces",
        "wifi_security": check_wifi_security(),
        "os": detect_os(),
        "firewall": detect_firewall(),
        "scan_time": scan_time
    }
    return summary




