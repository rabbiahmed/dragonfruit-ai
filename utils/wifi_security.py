# utils/wifi_security.py

import platform
import subprocess


def check_wifi_security():
    try:
        system = platform.system()

        if system == "Linux":
            output = subprocess.check_output("nmcli -f active,ssid,security dev wifi", shell=True, text=True)
            for line in output.splitlines():
                if "yes" in line.lower():
                    if "wpa" in line.lower() or "wpa2" in line.lower() or "wpa3" in line.lower():
                        return "🔐 WiFi is secured (WPA)"
                    else:
                        return "⚠️ WiFi is open or weakly secured"
            return "⚠️ No active WiFi connection found"

        elif system == "Windows":
            output = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
            if "Authentication" in output:
                if "WPA2" in output or "WPA3" in output:
                    return "🔐 WiFi is secured (WPA)"
                elif "Open" in output:
                    return "⚠️ WiFi is open or weakly secured"
            return "⚠️ No WiFi security information found"

        elif system == "Darwin":  # macOS
            output = subprocess.check_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I", shell=True, text=True)
            if "RSN" in output:
                return "🔐 WiFi is secured (WPA)"
            elif "None" in output:
                return "⚠️ WiFi is open or weakly secured"
            return "⚠️ No active WiFi connection found"

        return None

    except Exception as e:
        return f"Error checking WiFi security: {e}"

