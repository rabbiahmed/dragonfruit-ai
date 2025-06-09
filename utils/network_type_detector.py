# utils/network_type_detector.py

import platform
import subprocess
import psutil


def detect_network_type():
    system = platform.system()

    try:
        if system == "Linux":
            interfaces = subprocess.check_output("nmcli device status", shell=True, text=True)
            for line in interfaces.splitlines():
                if "wifi" in line.lower() and "connected" in line.lower():
                    return "Connected via WiFi"
                elif "ethernet" in line.lower() and "connected" in line.lower():
                    return "Connected via Ethernet"
            return "Connected (but interface type unknown)"

        elif system == "Windows":
            output = subprocess.check_output("netsh interface show interface", shell=True, text=True)
            if "Wi-Fi" in output and "Connected" in output:
                return "Connected via WiFi"
            elif "Ethernet" in output and "Connected" in output:
                return "Connected via Ethernet"
            return "Connected (but interface type unknown)"

        elif system == "Darwin":  # macOS
            output = subprocess.check_output("networksetup -getinfo Wi-Fi", shell=True, text=True)
            if "IP address" in output:
                return "Connected via WiFi"
            else:
                return "Connected via Ethernet or other"

    except Exception as e:
        return f"Error detecting network type: {e}"

    return "Could not determine network type"


def get_active_interfaces():
    active_interfaces = []
    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()

    for iface, data in stats.items():
        if data.isup and iface in addrs:
            # Skip loopback
            if iface.lower() in ["lo", "loopback"]:
                continue

            # Classify network type
            if "wl" in iface or "wifi" in iface.lower() or "wlan" in iface.lower():
                iface_type = "Wi-Fi"
            elif "en" in iface or "eth" in iface.lower():
                iface_type = "Ethernet"
            else:
                iface_type = "Other"

            active_interfaces.append(f"{iface} ({iface_type})")
    return active_interfaces
