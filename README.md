# DragonFruit AI

**DragonFruit AI** is a lightweight, intelligent cybersecurity assistant designed for personal and small business systems. It automates common security tasks such as:

* System monitoring
* Vulnerability assessment
* CVE lookup using the NVD API
* Optional local AI assistance (via LLMs like Mistral)

All of this can be triggered with just natural language input.

---

## Version 1.0.0 Features

* Analyze system and network health
* Assess system vulnerabilities
* Suggest system hardening improvements
* NLP-powered intent parser (hybrid rules + LLM)
* Lookup CVEs by ID or keyword (via NVD API)
* Optional AI assistant (locally run via Ollama)

---

### Version 1.1.0 — UI/UX Enhancements

* Modern chat bubble-style conversation layout
* Sidebar features:
  - Quick scan button
  - Real-time system status
  - Expandable diagnostics/info panels 

---

## 🚀 Getting Started

### Hardware Requirements

* Recommended: 16 GB RAM, modern CPU with AVX512 support
* \~50 GB available disk space
* GPU (optional, but helps with LLM performance)

### Software Requirements

* Python 3.7+
* [Ollama](https://ollama.com) for local LLM support

---

### 🔧 Install & Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the app:

```bash
streamlit run app.py
```

Run Ollama (in a separate terminal):

```bash
ollama serve
```

Start a model (e.g., Mistral):

```bash
ollama run mistral
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

> **Fair Use Notice**
> DragonFruit AI is free to use for personal and small business use.
> For integration into commercial products or large-scale services, please contact the maintainer to discuss licensing.

---

## 🤝 Contributions

Pull requests, feedback, and suggestions are welcome!
Feel free to open an issue or contribute directly via GitHub.

