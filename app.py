# app.py

# -- Import ---
import os
import time
import base64
import streamlit as st
from datetime import datetime
import html as html_escape
from streamlit.components.v1 import html
from utils.system_info import collect_system_summary
from utils.process_user_input import process_user_input

# --- Helper functions ---
# Load image and encode it
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Callback to handle input
def handle_input():
    user_input = st.session_state.user_input.strip()
    if not user_input:
        return

    now = time.time()
    last_time = st.session_state.get("last_input_time", 0)

    if user_input == st.session_state.get("last_user_input") and (now - last_time <= 5):
        return

    # Save user input
    st.session_state.last_user_input = user_input
    st.session_state.last_input_time = now
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append(("You", user_input, timestamp))

    # Process input
    result = process_user_input(user_input)
    ai_reply, extra, score, json_path = result if len(result) == 4 else (*result, None, None)

    # Save AI message
    if ai_reply:
        timestamp = datetime.now().strftime("%H:%M")
        if json_path:
            st.session_state.chat_history.append(("DragonFruit", ai_reply, timestamp, json_path))
        else:
            st.session_state.chat_history.append(("DragonFruit", ai_reply, timestamp))

    # Save additional data
    extra_data = extra or {}
    if json_path:
        extra_data["json_report_path"] = json_path
    st.session_state.extra_data = extra_data

    # Clear input field
    st.session_state.user_input = ""

# Automatically scrolls to bottom
def autoscroll_to_bottom():
    html("""
        <div id="chat-end" style="margin:0; padding:0;"></div>
        <script>
            setTimeout(function() {
                const chatEnd = document.getElementById("chat-end");
                if (chatEnd) {
                    chatEnd.scrollIntoView({ behavior: "smooth" });
                }
            }, 100);
        </script>
    """, height=0)

# Ensure timestamps for chat history entries
def migrate_chat_history():
    """Ensures all chat_history entries are 3-tuples by adding a default timestamp if missing."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        return
    migrated = []
    for item in st.session_state.chat_history:
        if len(item) == 3 or len(item) == 4:
            migrated.append(item)
        elif len(item) == 2:
            sender, message = item
            timestamp = datetime.now().strftime("%H:%M")
            migrated.append((sender, message, timestamp))
        elif len(item) == 1:
            sender = item[0]
            migrated.append((sender, "<no message>", datetime.now().strftime("%H:%M")))
        else:
            # Skip malformed entries
            continue
    st.session_state.chat_history = migrated

# Styled chat bubbles with timestamp
def render_chat(sender, message, timestamp, download_path=None):
    bubble_class = "user-bubble" if sender == "You" else "dragonfruit-bubble"

    safe_message = message if sender == "DragonFruit" else html_escape.escape(message)

    # Append download button only for DragonFruit
    if sender == "DragonFruit" and download_path:
        with open(download_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode()

        download_link = (
            f"<div style='margin-top: 12px;'>"
            f"<a download='vuln_report.json' "
            f"href='data:application/json;base64,{b64_data}' "
            f"style='text-decoration: none; color: white; background-color: #D12D6A; "
            f"padding: 6px 12px; border-radius: 5px; font-size: 14px; display: inline-block;'>"
            f"📄 Download Security Report (JSON)</a></div>"
        )

        safe_message += download_link

    # Compose the full bubble with timestamp and content
    formatted = f"""
    <div class="chat-bubble {bubble_class}">
        <div class="timestamp">{sender} • {timestamp}</div>
        <div>{safe_message}</div>
    </div>
    """
    st.markdown(formatted, unsafe_allow_html=True)

# --- Main screen: Initialization ---
st.set_page_config(page_title="DragonFruit AI", layout="wide")
icon_path = "assets/dragon_fruit.png"
icon_base64 = get_image_base64(icon_path) #icon for future use

# --- App header (left-aligned, custom color #B02A5A) ---
st.markdown("<h2 style='color:#B02A5A;'>DragonFruit</h2>", unsafe_allow_html=True)
st.subheader("Your cybersecurity assistant")

# --- Clear chat button ---
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history.clear()
    st.session_state.extra_data.clear()

# User input section
user_input = st.text_input(" ", placeholder="Ask anything", key="user_input", on_change=handle_input)

# Chat Layout
st.markdown("""
<style>
.chat-section {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 8px;
}

.chat-bubble {
    max-width: 80%;
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.4;
    word-wrap: break-word;
    height: auto !important;
    overflow: visible !important;
}

/* USER MESSAGE - right aligned */
.user-bubble {
    background-color: #f0f0f0;
    margin-left: auto;
    border-bottom-right-radius: 4px;
    text-align: right;
}

/* AI MESSAGE - left aligned */
.dragonfruit-bubble {
    background-color: #e6fff2;
    margin-right: auto;
    border-bottom-left-radius: 4px;
    text-align: left;
}

.timestamp {
    font-size: 11px;
    color: #888;
    margin-top: 2px;
    margin-bottom: 4px;
}

.chat-section > div {
    transition: all 0.2s ease-in-out;
}

iframe, .element-container {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
}
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#if "last_user_input" not in st.session_state:
#    st.session_state.last_user_input = ""

if "extra_data" not in st.session_state:
    st.session_state.extra_data = {}

# Display chat history
with st.container():
    for item in st.session_state.chat_history:
        if len(item) == 4:
            sender, message, timestamp, download_path = item
            render_chat(sender, message, timestamp, download_path=download_path)
        elif len(item) == 3:
            sender, message, timestamp = item
            render_chat(sender, message, timestamp)
    autoscroll_to_bottom()

# --- Sidebar: System Summary ---
# Logo, version
st.sidebar.image(icon_path, width=80)
st.sidebar.markdown("### DragonFruit AI")
st.sidebar.caption("🛡️ Version 1.1.0")
st.sidebar.markdown("---")

# Optional Quick Actions
if st.sidebar.button("🔄 Run Quick Scan"):
    start_time = time.time()

    # Run system summary directly
    system_info = collect_system_summary(start_time=start_time)
    system_info["scan_time"] = round(time.time() - start_time, 2)

    # Create a nicely formatted AI reply message
    quick_summary = (
        "Quick System Scan Summary\n\n"
        f"- **Internet**: {system_info.get('internet', 'Unknown')}\n"
        f"- **Connection Type**: {system_info.get('connection_type', 'No active interfaces')}\n"
        f"- **WiFi Security**: {system_info.get('wifi_security', 'Unknown')}\n"
        f"- **OS**: {system_info.get('os', 'Unknown')}\n"
        f"- **Firewall**: {system_info.get('firewall', 'Unknown')}\n"
        f"- **Scan Time**: {system_info.get('scan_time', 'N/A')}"
    )

    # Add to chat history
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append(("You", "Run quick system scan", timestamp))
    st.session_state.chat_history.append(("DragonFruit", quick_summary, timestamp))

    # Manually update system_info in extra_data (to update sidebar)
    st.session_state.extra_data["system_info"] = system_info

    # Force UI refresh to display updated chat and button
    st.experimental_rerun()

st.sidebar.markdown("---")

# System status
st.sidebar.header("⚙️ System Status")
if "system_info" in st.session_state.extra_data:
    info = st.session_state.extra_data["system_info"]
    # Use two spaces at end of each below line for emoji formating to new lines for each item
    st.sidebar.markdown(f"""
    🌐 **Internet**: {info.get('internet', 'Unknown')}  
    🔌 **Network**: {info.get('connection_type', 'Unknown')}  
    🔒 **WiFi Security**: {info.get('wifi_security', 'Unknown')}  
    🧱 **Firewall**: {info.get('firewall', 'Unknown')}  
    💻 **OS**: {info.get('os', 'Unknown')}  
    ⏱️ **Scan Time**: {info.get('scan_time', 'N/A')}s
    """)
else:
    st.sidebar.info("Run a scan or ask a question to populate system info.")
st.sidebar.markdown("---")

# Diagnostics (optional info)
with st.sidebar.expander("🧪 Diagnostics", expanded=False):
    st.text(f"Platform: {os.name}")
    st.text(f"User: {os.getenv('USER') or os.getenv('USERNAME')}")
    st.text(f"Session ID: {id(st.session_state)}")

# About / Help Section
with st.sidebar.expander("ℹ️ About DragonFruit"):
    st.markdown("""
    DragonFruit AI is a cybersecurity assistant powered by local LLMs.
    - 🔍 Real-time diagnostics
    - ⚠️ CVE lookups
    - 🤖 Mistral + Streamlit powered"""
    )
