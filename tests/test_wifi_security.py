# tests/test_wifi_security.py

import unittest
from unittest.mock import patch
from utils.wifi_security import check_wifi_security


class TestWifiSecurity(unittest.TestCase):

    @patch("utils.wifi_security.platform.system")
    @patch("utils.wifi_security.subprocess.check_output")
    def test_linux_secured_wifi(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "yes  MyWiFi   WPA2\n"
        result = check_wifi_security()
        self.assertIn("secured", result.lower())

    @patch("utils.wifi_security.platform.system")
    @patch("utils.wifi_security.subprocess.check_output")
    def test_linux_open_wifi(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "yes  MyWiFi   --\n"
        result = check_wifi_security()
        self.assertIn("open", result.lower())

    @patch("utils.wifi_security.platform.system")
    @patch("utils.wifi_security.subprocess.check_output")
    def test_linux_no_active_connection(self, mock_subproc, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subproc.return_value = "no   SomeWiFi WPA2\n"
        result = check_wifi_security()
        self.assertIn("no active", result.lower())


if __name__ == "__main__":
    unittest.main()
