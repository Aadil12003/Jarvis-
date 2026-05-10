"""
OS Execution Module ("The Hands").
Implements headless safety environments to prevent crashes on cloud deployments.
"""
import os
import sys
import webbrowser
import platform
import subprocess
from config import APPROVED_APPS, logger

SYSTEM_PLATFORM = platform.system().lower()

# Check for Headless Mode
IS_HEADLESS = False
if SYSTEM_PLATFORM != "windows" and "DISPLAY" not in os.environ and "WAYLAND_DISPLAY" not in os.environ:
    IS_HEADLESS = True
    logger.warning("No display environment found. Running in simulation mode.")

# Safely load GUI automation libraries only when a physical display exists
if not IS_HEADLESS:
    try:
        import pyautogui
        import ctypes
        pyautogui.FAILSAFE = True
    except Exception as e:
        logger.error(f"Graphical load failed: {e}")
        IS_HEADLESS = True

class OSAgent:
    def execute(self, structured_action: dict) -> tuple[bool, str]:
        action = structured_action.get("action", "unknown")
        params = structured_action.get("params", {}) or {}

        if IS_HEADLESS:
            return True, f"[SIMULATION MODE] Simulated desktop action: {action} with parameters: {params}"

        try:
            if action == "open_website":
                url = params.get("url", "")
                if url:
                    webbrowser.open(url if url.startswith("http") else f"https://{url}")
                    return True, f"Opened URL: {url}"
                return False, "No URL specified."
            
            elif action == "type_text":
                pyautogui.write(params.get("text", ""), interval=0.03)
                return True, "Typed text successfully."
                
            elif action == "press_key":
                pyautogui.press(params.get("key", "").lower())
                return True, "Pressed key."
                
            elif action == "hotkey":
                pyautogui.hotkey(*[k.lower() for k in params.get("keys", [])])
                return True, "Executed hotkey combo."
                
            elif action == "search_google":
                q = params.get("text", "")
                webbrowser.open(f"https://www.google.com/search?q={q}")
                return True, f"Searched Google for: {q}"
                
            elif action == "launch_app":
                app = params.get("app", "").lower()
                whitelist = APPROVED_APPS.get(SYSTEM_PLATFORM, {})
                if app in whitelist:
                    subprocess.Popen(whitelist[app], shell=True)
                    return True, f"Launched application: {app}"
                return False, f"App '{app}' is blocked by security whitelist."
                
            return False, "Unknown action bypass."
        except Exception as e:
            return False, f"OS Agent execution error: {str(e)}"
