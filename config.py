"""
Configuration and logging setup for JARVIS Assistant.
Supports local .env and Streamlit Cloud Secrets.
"""
import logging
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Retrieve API Key safely from Streamlit Cloud Secrets OR local environment variables
NVIDIA_API_KEY = ""
if "NVIDIA_API_KEY" in st.secrets:
    NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]
else:
    NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')

NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "meta/llama-3.1-70b-instruct" 

if not NVIDIA_API_KEY:
    logger.warning("NVIDIA_API_KEY not configured. Add it to Streamlit Secrets or your .env file.")

# Model configuration
TEMPERATURE = 0.1  # Low temperature for precise JSON parsing
MAX_TOKENS = 1000

# Streamlit UI Configuration
PAGE_TITLE = "JARVIS Assistant"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# UI Colors (Dark Cyan Theme)
PRIMARY_COLOR = "#00CED1"  # Dark Cyan
SECONDARY_COLOR = "#1F1F1F"  # Dark Gray
ACCENT_COLOR = "#FF6B6B"  # Red for alerts
SUCCESS_COLOR = "#51CF66"  # Green for success
WARNING_COLOR = "#FFD93D"  # Yellow for warnings

# Safe Mode Flag
SAFE_MODE = True

# OS Whitelisted Applications
APPROVED_APPS = {
    "windows": {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "explorer": "explorer.exe"
    },
    "darwin": {
        "calculator": "Calculator",
        "chrome": "Google Chrome"
    },
    "linux": {
        "calculator": "gnome-calculator",
        "chrome": "google-chrome"
    }
}

logger.info("Configuration loaded successfully")
