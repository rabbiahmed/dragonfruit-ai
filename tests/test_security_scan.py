# tests/test_security_scan.py

import unittest
from utils.security_scan import simple_port_scan


class TestSimplePortScan(unittest.TestCase):
    def test_default_ports_scan(self):
        # Should return a list of (port, status) tuples
        results = simple_port_scan()
        self.assertIsInstance(results, list)
        for item in results:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            port, is_open = item
            self.assertIsInstance(port, int)
            self.assertIsInstance(is_open, bool)

    def test_custom_ports(self):
        test_ports = [22, 12345]  # Assuming 22 may be open and 12345 likely closed
        results = simple_port_scan(ports=test_ports)
        scanned_ports = [r[0] for r in results]
        self.assertEqual(set(scanned_ports), set(test_ports))

    def test_invalid_host(self):
        # Should not raise error even with invalid host
        results = simple_port_scan(host="256.256.256.256")
        self.assertEqual(results, [("error", "Invalid host")])


if __name__ == "__main__":
    unittest.main()
