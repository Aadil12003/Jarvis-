"""
JARVIS - Desktop AI Assistant with Streamlit HUD
Dark Cyan Theme | Text-Based Control | OpenAI Integration
"""
import streamlit as st
import os
from openai import OpenAI
from config import logger, OPENAI_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS
from config import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, SUCCESS_COLOR, WARNING_COLOR
from speech_module import VoiceInputSystem
import pyautogui
import time

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
    
    .sidebar .sidebar-content {{
        background-color: #0F1635;
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

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'voice_system' not in st.session_state:
    st.session_state.voice_system = VoiceInputSystem()
if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=OPENAI_API_KEY)

# Header with HUD styling
st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-bottom: 2px solid {PRIMARY_COLOR}; margin-bottom: 30px;">
        <h1 class="hud-title">🤖 J.A.R.V.I.S</h1>
        <p style="color: {PRIMARY_COLOR}; font-size: 12px; letter-spacing: 1px;">JUST ANOTHER REMARKABLE VOICE INTERFACE SYSTEM</p>
        <p style="color: {WARNING_COLOR}; font-size: 11px;">TEXT MODE | PYTHON 3.14 COMPATIBLE | VOICE DISABLED</p>
    </div>
""", unsafe_allow_html=True)

# Layout: Main chat area + Sidebar
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"<h2 style='color: {PRIMARY_COLOR}; margin-top: 0;'>💬 COMMAND INTERFACE</h2>", unsafe_allow_html=True)
    
    # Conversation display
    conversation_container = st.container()
    with conversation_container:
        for i, msg in enumerate(st.session_state.conversation_history):
            if msg["role"] == "user":
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {SUCCESS_COLOR};'><strong>YOU:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-box' style='border-left: 4px solid {PRIMARY_COLOR};'><strong>JARVIS:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Input section
    st.markdown(f"<hr style='border-color: {PRIMARY_COLOR}; opacity: 0.3;'>", unsafe_allow_html=True)
    
    user_input = st.text_input(
        "Enter Command:",
        placeholder="Type your command here...",
        key="command_input"
    )
    
    col_submit, col_clear = st.columns(2)
    
    with col_submit:
        if st.button("▶ EXECUTE", use_container_width=True):
            if user_input.strip():
                # Add user message to history
                st.session_state.conversation_history.append({"role": "user", "content": user_input})
                logger.info(f"User input: {user_input}")
                
                try:
                    # Call OpenAI API
                    response = st.session_state.client.chat.completions.create(
                        model=MODEL,
                        messages=st.session_state.conversation_history,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS
                    )
                    
                    assistant_message = response.choices[0].message.content
                    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_message})
                    logger.info(f"JARVIS response: {assistant_message}")
                    
                except Exception as e:
                    error_msg = f"ERROR: {str(e)}"
                    st.session_state.conversation_history.append({"role": "assistant", "content": error_msg})
                    logger.error(f"API Error: {str(e)}")
                
                st.rerun()
    
    with col_clear:
        if st.button("🔄 CLEAR", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()

# Sidebar Control Panel
with col2:
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR};'>⚙️ CONTROL PANEL</h3>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='message-box'><strong>Status:</strong><br><span style='color: {SUCCESS_COLOR};'>● ONLINE</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='message-box'><strong>Mode:</strong><br><span style='color: {PRIMARY_COLOR};'>TEXT INPUT</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='message-box'><strong>Model:</strong><br><span style='color: {PRIMARY_COLOR};'>{MODEL}</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='message-box'><strong>Messages:</strong><br><span style='color: {WARNING_COLOR};'>{len(st.session_state.conversation_history)}</span></div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown(f"<h4 style='color: {ACCENT_COLOR};'>📋 Quick Commands</h4>", unsafe_allow_html=True)
    
    if st.button("⌨️ Type 'Hello'"):
        st.session_state.conversation_history.append({"role": "user", "content": "Hello, JARVIS!"})
        st.rerun()
    
    if st.button("📁 Open Explorer"):
        st.session_state.conversation_history.append({"role": "user", "content": "Open file explorer"})
        st.rerun()
    
    if st.button("🔐 System Info"):
        st.session_state.conversation_history.append({"role": "user", "content": "Show system information"})
        st.rerun()
    
    st.divider()
    
    st.markdown(f"<h4 style='color: {WARNING_COLOR};'>⚠️ Voice Status</h4>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: {ACCENT_COLOR}; font-size: 12px;'>Voice control disabled for Python 3.14 compatibility. Use text input above.</span>", unsafe_allow_html=True)
    
    st.divider()
    
    # Display API status
    if OPENAI_API_KEY:
        st.markdown(f"<span style='color: {SUCCESS_COLOR}; font-size: 11px;'>✓ API KEY CONFIGURED</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: {ACCENT_COLOR}; font-size: 11px;'>✗ API KEY MISSING - Add OPENAI_API_KEY to .env</span>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style="text-align: center; padding-top: 30px; border-top: 1px solid {PRIMARY_COLOR}; opacity: 0.5; font-size: 11px;">
        JARVIS © 2026 | Python 3.14 | Streamlit | OpenAI GPT-4
    </div>
""", unsafe_allow_html=True)

logger.info("JARVIS app initialized successfully")
