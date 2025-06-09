# tests/test_network_type_detector.py

import unittest
from unittest.mock import patch
from utils.network_type_detector import detect_network_type, get_active_interfaces


class TestNetworkTypeDetector(unittest.TestCase):

    # Patched platform.system(): To simulate different OS environments
    @patch("utils.network_type_detector.platform.system")
    # Patched subprocess.check_output: Because that's the real dependency used to detect network type
    @patch("utils.network_type_detector.subprocess.check_output")
    def test_detect_wifi_linux(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "wlan0 wifi connected\n"
        result = detect_network_type()
        self.assertIn("WiFi", result)

    @patch("utils.network_type_detector.platform.system")
    @patch("utils.network_type_detector.subprocess.check_output")
    def test_detect_ethernet_linux(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "eth0 ethernet connected\n"
        result = detect_network_type()
        self.assertIn("Ethernet", result)

    @patch("utils.network_type_detector.platform.system")
    @patch("utils.network_type_detector.subprocess.check_output")
    def test_detect_no_connection_linux(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "lo loopback disconnected\n"
        result = detect_network_type()
        self.assertIn("unknown", result.lower())

    def test_get_active_interfaces(self):
        interfaces = get_active_interfaces()
        self.assertIsInstance(interfaces, list, "Output should be a list")

        for iface in interfaces:
            self.assertIsInstance(iface, str, "Each interface should be a string")
            self.assertRegex(iface, r".+ \((Wi-Fi|Ethernet|Other)\)", "Interface type should be labeled")

            # It's acceptable for the list to be empty (e.g., all the interfaces are down)
            # But we should ensure it doesn't crash
            print("Detected active interfaces:", interfaces)

if __name__ == "__main__":
    unittest.main()

