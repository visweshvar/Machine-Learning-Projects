# console.py
# Interface for TTS engine
# Interacts solely with main tts module

# Add support for input() for Python 2
from builtins import input

from synthme import tts

if __name__ == "__main__":
	message = input("Message: ")
	tts.text_to_speech(message, debug=True, use_pronunciation_dict=True)
