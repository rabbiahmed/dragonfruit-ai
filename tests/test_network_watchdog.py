# tests/test_network_watchdog.py

import unittest
from utils.network_watchdog import get_active_ip_connections, get_connected_devices


class TestNetworkWatchdog(unittest.TestCase):
    def test_active_ip_connections(self):
        connections = get_active_ip_connections()
        self.assertIsInstance(connections, list)

    def test_connected_devices_format(self):
        devices = get_connected_devices()
        self.assertIsInstance(devices, list)
