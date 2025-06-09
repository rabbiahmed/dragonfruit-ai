# utils/security_commands.py

import getpass
import subprocess
from utils.security_scan import simple_port_scan


def run_security_command(command_name):
    if command_name == "open_ports":
        try:
            scan = simple_port_scan()
            readable = "\n".join([f"Port {p}: {'✅ Open' if is_open else '🔒 Closed'}" for p, is_open in scan])
            return f"🔍 Port Scan on localhost:\n{readable}"
        except Exception as e:
            return f"❌ Error running port scan: {e}"

    elif command_name == "active_connections":
        try:
            output = subprocess.check_output(["netstat", "-an"], stderr=subprocess.STDOUT, text=True, timeout=10)
            return f"🔍 Active Network Connections:\n\n```\n{output.strip()}\n```"
        except Exception as e:
            return f"❌ Error fetching connections: {e}"

    elif command_name == "current_user":
        try:
            try:
                username = getpass.getuser().strip()
            except (ImportError, KeyError, OSError) as e:
                username = subprocess.check_output(
                    ["whoami"], stderr=subprocess.STDOUT, text=True, timeout=5
                ).strip()
            return username
        except (subprocess.SubprocessError, Exception) as final_err:
            return f"Error determining user ({final_err})"

    return "Unsupported command."

