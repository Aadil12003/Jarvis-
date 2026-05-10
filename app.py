"""
JARVIS - Desktop AI Assistant with Streamlit HUD
Dark Cyan Theme | Cloud-Headless Safe | NVIDIA NIM Integration | Browser-Native Voice
"""
import streamlit as st
import os
import json
import time
from datetime import datetime
from config import logger, NVIDIA_API_KEY, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, SUCCESS_COLOR, WARNING_COLOR, SAFE_MODE
from speech_module import VoiceInputSystem
from ai_parser import JarvisBrain
from os_agent import OSAgent, IS_HEADLESS
from streamlit_mic_recorder import speech_to_text

# Configure Streamlit page
st.set_page_config(
    page_title="JARVIS Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Cyan HUD Theme with pulsing animations
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
        transform: scale(1.02);
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
""", unsafe_allow_html=True)

# Initialize session state variables
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
        <p style="color: {WARNING_COLOR}; font-size: 11px;">NVIDIA NIM DRIVEN | BROWSER-NATIVE SPEECH | DESKTOP CONTROL ENABLED</p>
    </div>
""", unsafe_allow_html=True)

# Layout: Main chat area + Sidebar
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"<h2 style='color: {PRIMARY_COLOR}; margin-top: 0;'>💬 COMMAND INTERFACE</h2>", unsafe_allow_html=True)
    
    if IS_HEADLESS:
        st.warning("🌐 Headless Cloud Environment Detected. Graphical actions will be simulated within the interface console below.")
    
    # Conversation Display Container
    conversation_container = st.container()
    with conversation_container:
        for msg in st.session_state.conversation_history:
            if msg["role"] == "user":
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {SUCCESS_COLOR};'><strong>YOU:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {PRIMARY_COLOR};'><strong>JARVIS:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Input section
    st.markdown(f"<hr style='border-color: {PRIMARY_COLOR}; opacity: 0.3;'>", unsafe_allow_html=True)
    
    # Text input override fallback
    user_text_command = st.text_input(
        "Enter Command:",
        placeholder="Type a manual command here (or use the voice cockpit button in the sidebar)...",
        key="command_input"
    )
    
    # Core Pipeline trigger
    command_to_process = None
    
    col_submit, col_clear = st.columns(2)
    with col_submit:
        if st.button("▶ EXECUTE MANUAL COMMAND", use_container_width=True):
            if user_text_command.strip():
                command_to_process = user_text_command.strip()
                st.session_state.conversation_history.append({"role": "user", "content": command_to_process})
    with col_clear:
        if st.button("🔄 PURGE SYSTEM SCREEN", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()

# Sidebar Cockpit
with col2:
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR}; margin-top: 0;'>⚙️ COCKPIT PANEL</h3>", unsafe_allow_html=True)
    
    status_label = "● Headless (Simulation)" if IS_HEADLESS else "● Headed (Local Active)"
    status_color = WARNING_COLOR if IS_HEADLESS else SUCCESS_COLOR
    st.markdown(f"<div class='message-box'><strong>Status:</strong><br><span style='color: {status_color}; font-weight: bold;'>{status_label}</span></div>", unsafe_allow_html=True)
    
    # Voice Activation Portal
    st.markdown("<div class='message-box'><strong>🎙️ Vocal Command Interface:</strong>", unsafe_allow_html=True)
    st.write("Click 'Listen', speak your command clearly, and click 'Stop' to parse.")
    
    # Native client-side audio capture widget
    browser_voice_transcript = speech_to_text(
        language='en', 
        start_prompt="🎙️ LISTEN", 
        stop_prompt="⏹️ STOP", 
        just_once=True, 
        use_container_width=True, 
        key='jarvis_speech_engine'
    )
    
    if browser_voice_transcript:
        command_to_process = browser_voice_transcript
        st.session_state.conversation_history.append({"role": "user", "content": f"[Voice Input]: {command_to_process}"})
        st.success(f"Recognized voice: '{command_to_process}'")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fast Action Buttons
    st.markdown(f"<h4 style='color: {WARNING_COLOR}; margin-top: 15px;'>📋 Quick Scenarios</h4>", unsafe_allow_html=True)
    if st.button("📁 Open YouTube"):
        command_to_process = "open youtube.com"
        st.session_state.conversation_history.append({"role": "user", "content": command_to_process})
    if st.button("💻 Search Python"):
        command_to_process = "Search google for python automation"
        st.session_state.conversation_history.append({"role": "user", "content": command_to_process})
    if st.button("🗒️ Open Notepad"):
        command_to_process = "launch notepad"
        st.session_state.conversation_history.append({"role": "user", "content": command_to_process})
        
    st.divider()
    if NVIDIA_API_KEY:
        st.markdown(f"<span style='color: {SUCCESS_COLOR}; font-weight: bold;'>✓ NVIDIA KEY CONFIGURED</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: {ACCENT_COLOR}; font-weight: bold;'>✗ NVIDIA KEY MISSING - Add NVIDIA_API_KEY to secrets</span>", unsafe_allow_html=True)

# Main Processing Engine Pipeline
if command_to_process:
    with st.spinner("🧠 J.A.R.V.I.S. is parsing voice commands..."):
        try:
            parsed_intent = st.session_state.brain.parse_intent(command_to_process)
            action = parsed_intent.get("action", "unknown")
            
            if action == "unknown":
                response_msg = "My core safety protocol rejected this command as a security risk or unknown syntax structure."
            else:
                success, execution_msg = st.session_state.executor.execute(parsed_intent)
                response_msg = f"Intent decoded: **{action}**\n\nSystem Response: {execution_msg}"
                
            st.session_state.conversation_history.append({"role": "assistant", "content": response_msg})
            st.rerun()
        except Exception as err:
            logger.error(f"Execution Error: {err}")
            st.session_state.conversation_history.append({"role": "assistant", "content": f"Failed executing command sequence: {err}"})
            st.rerun()

# Footer
st.markdown(f"""
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid {PRIMARY_COLOR}; opacity: 0.5; font-size: 11px; margin-top: 50px;">
        JARVIS © 2026 | Python 3.14 | Streamlit | Nvidia Llama-3.1 NIM
    </div>
""", unsafe_allow_html=True)
