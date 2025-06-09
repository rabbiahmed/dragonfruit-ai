# tests/test_ollama_llm.py

import unittest
import requests
from unittest.mock import patch, MagicMock
from utils.ollama_llm import ask_ollama


class TestAskOllama(unittest.TestCase):

    @patch("utils.ollama_llm.requests.post")
    def test_successful_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Hello from Mistral!"}
        mock_post.return_value = mock_response

        result = ask_ollama("Hello")
        self.assertEqual(result, "Hello from Mistral!")

    @patch("utils.ollama_llm.requests.post")
    def test_no_response_key(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        result = ask_ollama("What's up?")
        self.assertEqual(result, "Sorry, no response.")

    @patch("utils.ollama_llm.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = requests.RequestException("Connection refused")

        result = ask_ollama("Hi!")
        self.assertIn("⚠️ Error", result)
        self.assertIn("Connection refused", result)


if __name__ == "__main__":
    unittest.main()
