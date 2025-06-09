# utils/process_user_input.py

import time
from utils.system_info import collect_system_summary
from utils.system_metrics import get_system_metrics
from utils.security_commands import run_security_command
from utils.wifi_security import check_wifi_security
from utils.network_watchdog import get_active_ip_connections, summarize_connections
from utils.vulnerability_assessor import system_vulnerability_check
from utils.network_type_detector import detect_network_type
from utils.cve_lookup import lookup_cve
from utils.ollama_llm import ask_ollama
from utils.intent_parser import detect_intents_and_entities


def process_user_input(user_input: str):
    start_time = time.time()

    ai_reply_parts = []
    special_data = {}
    score = None
    json_path = None

    parsed = detect_intents_and_entities(user_input)
    intents = parsed["intents"]
    entities = parsed["entities"]

    if not intents and not entities.get("cve_ids"):
        # Fallback to LLM if no known intent or CVE
        ai_reply_parts.append(ask_ollama(user_input))
    else:
        for intent in intents:

            # Add another intent block for system information
            # it should include OS and system status
            if intent == "system_information":
                system_info = collect_system_summary()
                print(system_info)
                metrics = get_system_metrics()
                system_information = (
                    f"🖥️ System Information\n\n"
                    f"**OS**: {system_info.get('os', 'Unknown')}\n"
                    f"**CPU Usage:** {metrics['cpu']}%\n"
                    f"**Memory Usage:** {metrics['memory']}%\n"
                    f"**Disk Usage:** {metrics['disk']}%"
                )
                ai_reply_parts.append(system_information)

            elif intent == "system_status":
                metrics = get_system_metrics()
                system_status = (
                    f"🖥️ System Status\n\n"
                    f"**CPU Usage:** {metrics['cpu']}%\n"
                    f"**Memory Usage:** {metrics['memory']}%\n"
                    f"**Disk Usage:** {metrics['disk']}%"
                )
                ai_reply_parts.append(system_status)

            elif intent == "firewall_status":
                firewall_status = collect_system_summary(start_time).get("firewall", "Unknown")
                ai_reply_parts.append(f"🛡️ Firewall Status: {firewall_status}")

            elif intent == "network_type":
                connection_type = detect_network_type()
                ai_reply_parts.append(f" Connection Type: **{connection_type}**")

            elif intent == "wifi_security":
                ai_reply_parts.append(check_wifi_security())

            elif intent == "network_watchdog":
                connections = get_active_ip_connections()
                summary = summarize_connections(connections)
                summary_text = "🔍 Network Watchdog Report\n\n"
                summary_text += "\n".join(f"**{key}:** {value}" for key, value in summary.items())
                ai_reply_parts.append(summary_text)
                special_data["connections"] = connections

            elif intent == "vulnerability_check":
                score, report, suggestions, json_path = system_vulnerability_check()
                vuln_reply = "🛡️ System Vulnerability Check\n\n"
                vuln_reply += f"**Security Score:** {score}/100\n\n"
                for key, value in report.items():
                    vuln_reply += f"**{key}:** {value}\n"
                if suggestions:
                    vuln_reply += "\n💡 **Suggestions to Improve Security:**\n"
                    for suggestion in suggestions:
                        vuln_reply += f"- {suggestion}\n"
                ai_reply_parts.append(vuln_reply)

            elif intent == "open_ports":
                ai_reply_parts.append(run_security_command("open_ports"))

            elif intent == "cve_lookup" and entities.get("cve_ids"):
                cve_results = []
                for cve_id in entities["cve_ids"]:
                    cve_info = lookup_cve(cve_id)
                    cve_results.append(cve_info)
                ai_reply_parts.append("🔎 CVE Lookup Results\n\n" + "\n\n".join(cve_results))

        special_data["system_info"] = collect_system_summary(start_time)

    ai_reply = "\n\n".join(ai_reply_parts)
    return ai_reply, special_data, score, json_path

