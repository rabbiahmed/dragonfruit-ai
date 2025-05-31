# dragonfruit-ai
DragonFruit AI is a lightweight, intelligent Cybersecurity assistant for personal and small business systems. It helps automate blue team tasks like system status summary, port scanning, firewall checks, vulnerability lookup, and more — all with a single natural language input. It aims to:
- Simplify common blue team tasks for non-experts
- Provide fast, meaningful system insights
- Reduce time spent on threat investigation
- Empower SMBs with accessible security automation

## Features (Version 1.0)
- AI assistant
- Detect open ports and firewall status
- Analyze system and network health
- Lookup CVEs by ID
- Monitor active network connections
- Assess Wi-Fi security level
- NLP-powered intent parser (hybrid rules + LLM)

## Getting Started
HW Requirements:
Ollama, can run AI models locally, generally requires 16 GB RAM along with recommended 50 GB disk space and modern CPU with AVX512 support. While a GPU isn’t mandatory, it can significantly improve performance.

SW Requirements:
Python 3.7+

Install dependencies:
```
pip install -r requirements.txt
```

Run the app:
```
streamlit run app.py
```

Run Ollama:
Try this after installing ollama, run
```
ollama serve
```
let that be there. 

Open another shell and run ollama, as an example:
```
ollama run mistral
```
## License

This project is licensed under the MIT License. See `LICENSE` file for full terms.

> Fair Use Notice:
> DragonFruit AI is free to use for personal and small business use.
> If you intend to integrate this project into a commercial product or service at scale, please contact the maintainer to discuss licensing terms.

## Contributions
Pull requests, bug fixes, feedback, and feature suggestions are welcome!
