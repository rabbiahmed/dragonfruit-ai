# utils/network_watchdog.py

import psutil
import socket
import subprocess
import platform
import re
from collections import Counter


# Get active network socket connections on the local machine
def get_active_ip_connections():
    conns = psutil.net_connections(kind='inet')
    data = []

    for c in conns:
        if c.status != psutil.CONN_NONE:
            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
            proto = "TCP" if c.type == socket.SOCK_STREAM else "UDP"
            try:
                pname = psutil.Process(c.pid).name() if c.pid else "N/A"
            except Exception:
                pname = "N/A"

            data.append({
                "PID": c.pid,
                "Process": pname,
                "Protocol": proto,
                "Local Address": laddr,
                "Remote Address": raddr,
                "Status": c.status
            })
    return data


def get_connected_devices():
    system = platform.system().lower()
    devices = []

    try:
        if system == "windows":
            output = subprocess.check_output("arp -a", shell=True).decode()
            pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9\-]+)\s+\w+"
        else:  # macOS/Linux
            output = subprocess.check_output(["arp", "-a"]).decode()
            pattern = r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([a-fA-F0-9:]+)"

        matches = re.findall(pattern, output)

        for ip, mac in matches:
            devices.append({"IP": ip, "MAC": mac})

    except Exception as e:
        devices.append({"Error": f"Failed to retrieve devices: {e}"})

    return devices


def summarize_connections(connections):
    network_summary = {"Total Connections": len(connections)}

    remote_ips = [c["Remote Address"].split(":")[0] for c in connections if c["Remote Address"]]
    network_summary["Unique Remote IPs"] = len(set(remote_ips))

    protocols = [c["Protocol"] for c in connections]
    network_summary["Protocol Breakdown"] = dict(Counter(protocols))

    ports = [c["Local Address"].split(":")[-1] for c in connections if c["Local Address"]]
    network_summary["Top Ports"] = dict(Counter(ports).most_common(3))

    pids = [str(c["PID"]) for c in connections if c["PID"]]
    network_summary["Top PIDs"] = dict(Counter(pids).most_common(3))

    return network_summary

