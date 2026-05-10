"""
Speech Module (Browser-Native Processing).
Voice operations are securely captured using HTML5 browser-native inputs.
"""
from config import logger

class VoiceInputSystem:
    def __init__(self):
        logger.info("Voice System initialized in Browser Integration Mode.")
        
    def capture_voice(self) -> tuple[bool, str]:
        """
        No-op fallback: Speech capture is executed client-side via Streamlit components.
        """
        return False, "Using browser speech recognition interface."
