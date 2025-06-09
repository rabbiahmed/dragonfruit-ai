# tests/test_cve_lookup.py

import unittest
import requests
from unittest.mock import patch, MagicMock
from utils.cve_lookup import lookup_cve


class TestCVELookup(unittest.TestCase):

    @patch("utils.cve_lookup.requests.get")
    def test_successful_lookup(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-2024-12345",
                        "descriptions": [{"lang": "en", "value": "Example vulnerability"}],
                        "metrics": {
                            "cvssMetricV31": [{
                                "cvssData": {
                                    "baseScore": 9.8,
                                    "baseSeverity": "CRITICAL"
                                }
                            }]
                        },
                        "published": "2024-05-01T00:00Z",
                        "lastModified": "2024-05-05T00:00Z"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        result = lookup_cve("test-keyword")
        self.assertIn("CVE-2024-12345", result)
        self.assertIn("Example vulnerability", result)
        self.assertIn("Severity: **CRITICAL**", result)
        self.assertIn("CVSS Score: **9.8**", result)
        self.assertIn("Published: 2024-05-01", result)

    @patch("utils.cve_lookup.requests.get")
    def test_no_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"vulnerabilities": []}
        mock_get.return_value = mock_response

        result = lookup_cve("nonexistent-keyword")
        self.assertIn("No CVEs found", result)

    @patch("utils.cve_lookup.requests.get")
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network failure")

        result = lookup_cve("nginx")
        self.assertIn("Error querying NVD", result)

    @patch("utils.cve_lookup.requests.get")
    def test_missing_fields_fallbacks(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "vulnerabilities": [
                {
                    "cve": {
                        # No id, no English description, no metrics
                        "descriptions": [{"lang": "jp", "value": "Japanese only"}],
                        "published": "N/A"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        result = lookup_cve("test")
        self.assertIn("**N/A**", result)
        self.assertIn("No description available", result)
        self.assertIn("Severity: **N/A**", result)
        self.assertIn("CVSS Score: **N/A**", result)


if __name__ == "__main__":
    unittest.main()
