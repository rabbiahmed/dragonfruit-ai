# tests/test_process_user_input.py

import unittest
from utils.process_user_input import process_user_input


class TestProcessUserInput(unittest.TestCase):

    def test_open_ports(self):
        reply, extra, *_ = process_user_input("Check open ports")
        self.assertIn("port", reply.lower()) # assertIn is used to detect phrases in replies

    def test_wifi_security(self):
        reply, _, *_ = process_user_input("Is my WiFi secure?")
        self.assertTrue("secure" in reply.lower() or "open" in reply.lower())

    def test_network_type(self):
        reply, _, *_ = process_user_input("Tell me if I'm on WiFi or Ethernet")
        self.assertTrue("wifi" in reply.lower() or "ethernet" in reply.lower())

    def test_system_status(self):
        reply, _, *_ = process_user_input("Show system status: CPU, memory, disk")
        self.assertIn("cpu", reply.lower())
        self.assertIn("memory", reply.lower())
        self.assertIn("disk", reply.lower())

    def test_current_user(self):
        reply, _, *_ = process_user_input("Who am I?")
        self.assertTrue(len(reply.strip()) > 0)

    def test_securities_variants(self):
        inputs = [
            "check securities",
            "What is the security status?"
        ]
        for user_input in inputs:
            reply, _, score, _ = process_user_input(user_input)
            self.assertIsInstance(reply, str)
            self.assertIsNotNone(score)
            self.assertIn("security score", reply.lower())

    def test_vulnerabilities_singular(self):
        reply, _, score, _ = process_user_input("Check for vulnerability")
        self.assertIsInstance(score, (int, float))
        self.assertIn("vulnerability", reply.lower())

    def test_vulnerabilities_plural(self):
        reply, _, score, _ = process_user_input("Check for vulnerabilities")
        self.assertIsInstance(score, (int, float))
        self.assertTrue("vulnerability" in reply.lower() or "vulnerabilities" in reply.lower())

    def test_network_watchdog_summary(self):
        reply, extra, *_ = process_user_input("Give me a connection summary")
        self.assertIn("network watchdog", reply.lower())
        self.assertIn("connections", extra)

    def test_multiple_intents(self):
        reply, extra, score, _ = process_user_input("Check open ports and vulnerabilities.")
        self.assertIn("port", reply.lower())
        self.assertIn("vulnerability", reply.lower())
        self.assertIsNotNone(score)

    def test_conjunctions_and_punctuation(self):
        reply, _, *_ = process_user_input("Scan my ports and show CPU and memory usage.")
        self.assertIn("port", reply.lower())
        self.assertTrue(
            "cpu" in reply.lower() or "memory" in reply.lower() or "disk" in reply.lower()
        )

    def test_unknown_fallback(self):
        reply, _, *_ = process_user_input("What is the meaning of cyber life?")
        self.assertIsInstance(reply, str)
        self.assertGreater(len(reply), 0)


if __name__ == "__main__":
    unittest.main()

