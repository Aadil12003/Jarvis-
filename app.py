"""
JARVIS - Desktop AI Assistant with Streamlit HUD
Dark Cyan Theme | Cloud-Headless Safe | NVIDIA NIM Integration
"""
import streamlit as st
import os
import json
import time
from config import logger, NVIDIA_API_KEY, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, SUCCESS_COLOR, WARNING_COLOR, SAFE_MODE
from speech_module import VoiceInputSystem
from ai_parser import JarvisBrain
from os_agent import OSAgent, IS_HEADLESS

# Configure Streamlit page
st.set_page_config(
    page_title="JARVIS Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Cyan HUD Theme
st.markdown(f"""
    <style>
    :root {{
        --primary: {PRIMARY_COLOR};
        --secondary: {SECONDARY_COLOR};
        --accent: {ACCENT_COLOR};
        --success: {SUCCESS_COLOR};
        --warning: {WARNING_COLOR};
    }}
    
    body {{
        background-color: #0A0E27;
        color: {PRIMARY_COLOR};
        font-family: 'Courier New', monospace;
    }}
    
    .main {{
        background-color: #0A0E27;
        background-image: 
            linear-gradient(0deg, transparent 24%, rgba(0, 206, 209, 0.05) 25%, rgba(0, 206, 209, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 206, 209, 0.05) 75%, rgba(0, 206, 209, 0.05) 76%, transparent 77%, transparent),
            linear-gradient(90deg, transparent 24%, rgba(0, 206, 209, 0.05) 25%, rgba(0, 206, 209, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 206, 209, 0.05) 75%, rgba(0, 206, 209, 0.05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }}
    
    .stTextInput > div > div > input {{
        background-color: #1a1a2e;
        color: {PRIMARY_COLOR};
        border: 2px solid {PRIMARY_COLOR};
        border-radius: 4px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        box-shadow: 0 0 10px rgba(0, 206, 209, 0.3);
    }}
    
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: #0A0E27;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0, 206, 209, 0.5);
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 0 20px rgba(0, 206, 209, 0.8);
        transform: scale(1.05);
    }}
    
    .message-box {{
        background-color: #1a1a2e;
        border: 1px solid {PRIMARY_COLOR};
        border-radius: 4px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 0 8px rgba(0, 206, 209, 0.2);
        font-family: 'Courier New', monospace;
    }}
    
    .hud-title {{
        color: {PRIMARY_COLOR};
        text-shadow: 0 0 10px {PRIMARY_COLOR};
        font-weight: bold;
        letter-spacing: 2px;
    }}
    </style>
""", unsafe_allow_html=True) #

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'voice_system' not in st.session_state:
    st.session_state.voice_system = VoiceInputSystem()
if 'brain' not in st.session_state:
    st.session_state.brain = JarvisBrain()
if 'executor' not in st.session_state:
    st.session_state.executor = OSAgent()

# Header with HUD styling
st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-bottom: 2px solid {PRIMARY_COLOR}; margin-bottom: 30px;">
        <h1 class="hud-title">🤖 J.A.R.V.I.S</h1>
        <p style="color: {PRIMARY_COLOR}; font-size: 12px; letter-spacing: 1px;">JUST ANOTHER REMARKABLE VOICE INTERFACE SYSTEM</p>
        <p style="color: {WARNING_COLOR}; font-size: 11px;">NVIDIA NIM DRIVEN | CLOUD ACCESSIBLE | DESKTOP CONTROL ENABLED</p>
    </div>
""", unsafe_allow_html=True) #

# Layout: Main chat area + Sidebar
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"<h2 style='color: {PRIMARY_COLOR}; margin-top: 0;'>💬 COMMAND INTERFACE</h2>", unsafe_allow_html=True) #
    
    if IS_HEADLESS:
        st.warning("🌐 Headless Cloud Environment Detected. Graphical actions will be simulated within the interface console below.")
    
    # Conversation display
    conversation_container = st.container()
    with conversation_container:
        for i, msg in enumerate(st.session_state.conversation_history):
            if msg["role"] == "user":
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {SUCCESS_COLOR};'><strong>YOU:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {PRIMARY_COLOR};'><strong>JARVIS:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Input section
    st.markdown(f"<hr style='border-color: {PRIMARY_COLOR}; opacity: 0.3;'>", unsafe_allow_html=True) #
    
    user_input = st.text_input(
        "Enter Command:",
        placeholder="Type your command here (e.g., 'open google', 'launch notepad')...",
        key="command_input"
    )
    
    col_submit, col_clear = st.columns(2)
    
    with col_submit:
        if st.button("▶ EXECUTE", use_container_width=True):
            if user_input.strip():
                st.session_state.conversation_history.append({"role": "user", "content": user_input})
                logger.info(f"User input: {user_input}")
                
                try:
                    # 1. Parse natural command to JSON
                    parsed_intent = st.session_state.brain.parse_intent(user_input)
                    action = parsed_intent.get("action", "unknown")
                    
                    if action == "unknown":
                        response_msg = "Command intent could not be identified or flagged safety validation parameters."
                    else:
                        # 2. Execute via OS Engine (Headless Safe)
                        success, detail_msg = st.session_state.executor.execute(parsed_intent)
                        response_msg = f"Intent matches action type: **{action}**.\n\nResult details: {detail_msg}"
                    
                    st.session_state.conversation_history.append({"role": "assistant", "content": response_msg})
                    
                except Exception as e:
                    error_msg = f"ERROR: {str(e)}"
                    st.session_state.conversation_history.append({"role": "assistant", "content": error_msg})
                    logger.error(f"Execution Error: {str(e)}")
                
                st.rerun()
    
    with col_clear:
        if st.button("🔄 CLEAR", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()

# Sidebar Control Panel
with col2:
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR};'>⚙️ CONTROL PANEL</h3>", unsafe_allow_html=True) #
    
    status_label = "● SIMULATING" if IS_HEADLESS else "● ONLINE"
    status_color = WARNING_COLOR if IS_HEADLESS else SUCCESS_COLOR
    st.markdown(f"<div class='message-box'><strong>Status:</strong><br><span style='color: {status_color};'>{status_label}</span></div>", unsafe_allow_html=True) #
    
    st.markdown(f"<div class='message-box'><strong>System Mode:</strong><br><span style='color: {PRIMARY_COLOR};'>TEXT CONTROL</span></div>", unsafe_allow_html=True) #
    
    st.markdown(f"<div class='message-box'><strong>Parser:</strong><br><span style='color: {PRIMARY_COLOR};'>NVIDIA NIM Llama-3.1</span></div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown(f"<h4 style='color: {ACCENT_COLOR};'>📋 Quick Commands</h4>", unsafe_allow_html=True) #
    
    if st.button("📁 Open Website"):
        st.session_state.conversation_history.append({"role": "user", "content": "open youtube.com"})
        st.rerun()
    
    if st.button("💻 Search Python"):
        st.session_state.conversation_history.append({"role": "user", "content": "Search google for python automation"})
        st.rerun()
    
    if st.button("🗒️ Open Notepad"):
        st.session_state.conversation_history.append({"role": "user", "content": "launch notepad"})
        st.rerun()
    
    st.divider()
    
    if NVIDIA_API_KEY:
        st.markdown(f"<span style='color: {SUCCESS_COLOR}; font-size: 11px;'>✓ NVIDIA KEY CONFIGURED</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: {ACCENT_COLOR}; font-size: 11px;'>✗ NVIDIA KEY MISSING - Add NVIDIA_API_KEY to .env</span>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid {PRIMARY_COLOR}; opacity: 0.5; font-size: 11px;">
        JARVIS © 2026 | Python 3.14 | Streamlit | Nvidia Llama-3.1 NIM
    </div>
""", unsafe_allow_html=True) #
