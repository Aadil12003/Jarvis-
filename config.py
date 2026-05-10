"""
Configuration and logging setup for JARVIS Assistant.
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

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set. Please add it to your .env file.")

# Model configuration
MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 2000

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

logger.info("Configuration loaded successfully")
