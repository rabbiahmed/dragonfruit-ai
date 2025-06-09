import unittest
from unittest.mock import patch
from utils import security_commands


class TestSecurityCommands(unittest.TestCase):

    @patch("utils.security_commands.simple_port_scan")
    def test_open_ports(self, mock_scan):
        mock_scan.return_value = [(22, True), (80, False)]
        result = security_commands.run_security_command("open_ports")
        self.assertIn("Port 22: ✅ Open", result)
        self.assertIn("Port 80: 🔒 Closed", result)

    @patch("subprocess.check_output")
    def test_active_connections(self, mock_subproc):
        mock_subproc.return_value = "tcp        0      0 0.0.0.0:22      0.0.0.0:*       LISTEN"
        result = security_commands.run_security_command("active_connections")
        self.assertIn("Active Network Connections", result)
        self.assertIn("tcp", result)

    @patch("getpass.getuser")
    def test_current_user_success(self, mock_getuser):
        mock_getuser.return_value = "testuser"
        result = security_commands.run_security_command("current_user")
        self.assertEqual(result, "testuser")

    @patch("getpass.getuser", side_effect=OSError("getuser failed"))
    @patch("subprocess.check_output")
    def test_current_user_fallback(self, mock_subproc, mock_getuser):
        mock_subproc.return_value = "fallbackuser"
        result = security_commands.run_security_command("current_user")
        self.assertEqual(result, "fallbackuser")

    @patch("getpass.getuser", side_effect=OSError("getuser failed"))
    @patch("subprocess.check_output", side_effect=Exception("whoami failed"))
    def test_current_user_failure(self, mock_subproc, mock_getuser):
        result = security_commands.run_security_command("current_user")
        self.assertIn("Error determining user", result)

    def test_unsupported_command(self):
        result = security_commands.run_security_command("invalid_command")
        self.assertEqual(result, "Unsupported command.")


if __name__ == "__main__":
    unittest.main()
