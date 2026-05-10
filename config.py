"""
Configuration and logging setup for JARVIS Assistant.
Supports NVIDIA NIM API out of the box.
"""
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# NVIDIA API Configuration (Using OpenAI-compatible client schema)
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "meta/llama-3.1-70b-instruct" 

if not NVIDIA_API_KEY:
    logger.warning("NVIDIA_API_KEY not set. Please add it to your .env file.")

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
