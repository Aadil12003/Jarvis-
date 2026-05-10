"""
Speech Module (Text Fallback Mode).
Voice operations are disabled due to Python 3.14 binary incompatibilities.
"""

from config import logger


class VoiceInputSystem:
    def __init__(self):
        logger.info("Voice System initialized in Text Fallback Mode.")

    def capture_voice(self) -> tuple[bool, str]:
        """
        Fallback method returning a clean message advising the user to use text input.
        """
        logger.warning("Voice capture attempted but is disabled in this environment.")
        return (
            False,
            "Voice control is disabled. Please type your command in the input console below.",
        )
