"""
AI Intent Parser Module.
Communicates with NVIDIA API and parses inputs into actionable JSON structures.
"""
import json
import re
from openai import OpenAI
from config import NVIDIA_API_KEY, NVIDIA_API_BASE, NVIDIA_MODEL, logger

class JarvisBrain:
    def __init__(self):
        # Set a placeholder key if empty to prevent the OpenAI client from raising initialization credential exceptions
        resolved_key = NVIDIA_API_KEY if NVIDIA_API_KEY else "dummy_key_unconfigured"
        
        self.client = OpenAI(
            base_url=NVIDIA_API_BASE,
            api_key=resolved_key
        )
        
    def _get_system_prompt(self) -> str:
        return """You are an OS-level desktop command dispatcher. 
Convert human requests into a strict single JSON format execution command.

You must match the command to one of these valid action types:
1. "open_website" (params: "url")
2. "type_text" (params: "text")
3. "press_key" (params: "key")
4. "hotkey" (params: "keys" as array of strings, e.g. ["ctrl", "alt", "del"])
5. "system_volume" (params: "amount" - integer 0 to 100, "direction" - 'up' or 'down')
6. "launch_app" (params: "app" - "chrome", "notepad", "calculator", "explorer")
7. "search_google" (params: "text")
8. "unknown" (no params)

SAFETY CRITICAL RULE:
If the user requests dangerous actions (terminals, shell execution, deleting system files, bash, cmd), change action to "unknown".

Return ONLY raw parseable JSON matching this schema:
{
  "action": "action_name",
  "params": {
    "url": "optional_string",
    "text": "optional_string",
    "key": "optional_string",
    "keys": ["optional_array"],
    "direction": "optional_string",
    "amount": 0,
    "app": "optional_string"
  }
}
Do not return markdown or explanation text."""

    def parse_intent(self, user_command: str) -> dict:
        if not NVIDIA_API_KEY:
            return {"action": "unknown", "params": {"text": "NVIDIA API Key not configured. Please add it to your Streamlit Cloud secrets."}}
            
        try:
            response = self.client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_command}
                ],
                temperature=0.1,
                max_tokens=300
            )
            raw_content = response.choices[0].message.content.strip()
            cleaned_content = re.sub(r"^```json\s*|\s*```$", "", raw_content, flags=re.MULTILINE).strip()
            return json.loads(cleaned_content)
        except Exception as e:
            logger.error(f"Error parsing intent: {e}")
            return {"action": "unknown", "params": {"text": str(e)}}
