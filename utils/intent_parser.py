# utils/intent_parser.py

import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Ensure required NLTK data is downloaded
try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('wordnet')
    nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Map each intent to its synonyms/phrases
INTENT_KEYWORDS = {
    "system_status": ["cpu", "memory", "disk", "performance", "usage", "system status", "system load"],
    "system_information": ["os", "linux", "system info", "mac", "windows"],
    "network_type": [
            "ethernet", "wifi", "wi-fi", "network type", "connections type", "wired", "wireless", "am i on wifi",
            "am i on ethernet", "connection overview"],
    "wifi_security": ["wifi", "wi-fi", "wireless", "internet safety", "network password"],
    "network_watchdog": [
        "network", "connections", "watchdog", "netstat", "active connections", "ip traffic",
        "connection summary", "network summary", "network activity", "connection overview"],
    "vulnerability_check": ["vulnerability", "vulnerabilities", "secure", "security check", "weakness", "scan system",
                            "scan", "scanning", "security status", "securities", "vpn"],
    "open_ports": ["port", "ports", "portscan"],
    "firewall_status": ["firewall", "ufw", "iptables", "fire wall"],
    "cve_lookup": ["cve", "vulnerability id", "lookup cve", "search cve"],
}

CVE_REGEX = r"\bCVE-\d{4}-\d{4,7}\b"


def tokenize_and_normalize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return tokens


def detect_intents_and_entities(user_input):
    tokens = tokenize_and_normalize(user_input)
    cleaned_text = " ".join(tokens)
    token_set = set(tokens)

    detected_intents = []
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            keyword_tokens = keyword.lower().split()
            if all(k in token_set for k in keyword_tokens) or keyword in cleaned_text:
                detected_intents.append(intent)
                break

    # CVE Detection via regex
    cve_ids = re.findall(CVE_REGEX, user_input, flags=re.IGNORECASE)
    if cve_ids:
        detected_intents.append("cve_lookup")

    return {
        "intents": list(set(detected_intents)),
        "entities": {"cve_ids": cve_ids}
    }

