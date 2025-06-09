# tests/test_system_info.py

import unittest
from unittest.mock import patch
from utils.system_metrics import get_system_metrics
from utils.security_commands import run_security_command
from utils.system_info import (check_internet_connectivity, collect_system_summary, detect_os)


class TestSystemInfo(unittest.TestCase):

    def test_get_system_metrics_keys(self):
        metrics = get_system_metrics()
        self.assertIn("cpu", metrics)
        self.assertIn("memory", metrics)
        self.assertIn("disk", metrics)
        self.assertIsInstance(metrics["cpu"], (int, float))
        self.assertIsInstance(metrics["memory"], (int, float))
        self.assertIsInstance(metrics["disk"], (int, float))

    def test_run_security_command_valid(self):
        result = run_security_command("current_user")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result.strip(), "")

    def test_check_internet_connectivity(self):
        result = check_internet_connectivity()
        self.assertIn(result, [True, False])  # result must be boolean

    def test_collect_system_summary_keys(self):
        summary = collect_system_summary()
        self.assertIn("internet", summary)
        self.assertIn("connection_type", summary)
        self.assertIn("wifi_security", summary)
        self.assertIn("firewall", summary)
        self.assertIn("OS", summary)
        self.assertIn("scan_time", summary)

    def test_detect_os_returns_string(self):
        os_name = detect_os()
        self.assertIsInstance(os_name, str)
        self.assertNotEqual(os_name.strip(), "")

    # Edge Cases

    @patch("utils.system_info.socket.socket")
    def test_check_internet_connectivity_offline(self, mock_socket):
        mock_socket.return_value.connect.side_effect = OSError("Network unreachable")
        self.assertFalse(check_internet_connectivity())

    @patch("utils.system_info.detect_firewall")
    @patch("utils.system_info.check_wifi_security")
    @patch("utils.system_info.detect_network_type")
    @patch("utils.system_info.check_internet_connectivity", return_value=False)
    def test_collect_system_summary_offline(
        self, mock_net, mock_type, mock_wifi, mock_firewall
    ):
        mock_type.return_value = "Unknown"
        mock_wifi.return_value = "Unknown"
        mock_firewall.return_value = "Off"

        summary = collect_system_summary()
        self.assertEqual(summary["internet"], "Disconnected")
        self.assertEqual(summary["connection_type"], "Unknown")
        self.assertEqual(summary["wifi_security"], "Unknown")
        self.assertEqual(summary["firewall"], "Off")

    @patch("utils.system_info.platform.system", return_value="Darwin")
    @patch("utils.system_info.platform.mac_ver", return_value=("13.4.1", ("", "", ""), ""))
    def test_detect_os_mac(self, mock_ver, mock_sys):
        os_name = detect_os()
        self.assertIn("macOS", os_name)

    @patch("utils.system_info.platform.system", return_value="Windows")
    @patch("utils.system_info.platform.release", return_value="10")
    def test_detect_os_windows(self, mock_release, mock_sys):
        os_name = detect_os()
        self.assertIn("Windows 10", os_name)

    @patch("utils.system_info.platform.system", return_value="Linux")
    @patch("utils.system_info.distro.name", return_value="Ubuntu 22.04 LTS")
    def test_detect_os_linux(self, mock_distro, mock_sys):
        os_name = detect_os()
        self.assertIn("Ubuntu", os_name)


if __name__ == "__main__":
    unittest.main()

