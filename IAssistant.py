from gi.repository import Gtk, Gdk
from ollama import chat
from ollama import ChatResponse

from audio_recorder import AudioRecorder
from transcription_manager import TranscriptionManager
from tts_manager import TTSManager

from utils import handle_clipboard_text
import clipboard

import prompt as prompt
from pprint import pprint
import json
from datetime import datetime
import re


class IAssistant:
    def __init__(
        self,
        transcriber_model: str = "openai/whisper-large-v3-turbo",  # "openai/whisper-large-v3"
        transcriber_engine: str = "TransformersWhisper",
        model: str = "llama3.2:3b",
        tts_engine: str = "piper",
        tts_model: str = "voice_en_1",
    ):
        self.transcriber_model = transcriber_model
        self.transcriber_engine = transcriber_engine
        self.tts_model = tts_model
        self.tts_engine = tts_engine
        self.model = model
        self.messages = []
        self.clipboard_text = None
        self.last_clipboard_text = None
        self.clipboard_image = None
        self.system_prompt = "default_prompt"
        self.stop_action = False
        self.recorder = None
        self.transcriber = None
        self.tts = None
        self.state = "waiting"
        self.language = "en"

    def init_recoder(self, verbose=True):
        self.recorder = AudioRecorder(verbose)

    def init_transcriber(self, verbose=True):
        self.transcriber = TranscriptionManager(self, verbose)
        print(
            f"transcritpion engine {self.transcriber_engine} initialized {self.transcriber_model}"
        )

    def init_tts(self, verbose=True):
        self.tts = TTSManager(self, verbose)
        print(f"TTS engine {self.tts_engine} initialized with {self.tts_model}")

    def set_prompt(self, message: str = None):
        if not self.messages:
            self.messages.append(
                {
                    "role": "system",
                    "content": prompt.get_system_prompt_message(self.system_prompt),
                }
            )
        self.clipboard_text = clipboard.paste()
        message = handle_clipboard_text(self, message)
        self.messages.append({"role": "user", "content": message})

    def get_completion(self):
        response = chat(model=self.model, messages=self.messages)
        self.messages.append({"role": "user", "content": response.message.content})
        return response.message.content

    import re

    def postprocess_response(self,response):
        """
        Extracts the text within <spoken> and <clipboard> tags from the LLM response.
        Parameters:
            response (str): The LLM response containing <spoken> and <clipboard> tags.
        Returns:
            dict: A dictionary with keys 'spoken' and 'clipboard' containing the extracted text.
        """
        spoken_match = re.search(r"<spoken>(.*?)</spoken>", response, re.DOTALL)
        clipboard_match = re.search(
            r"<clipboard>(.*?)</clipboard>", response, re.DOTALL
        )
        return {
            "spoken": spoken_match.group(1).strip() if spoken_match else None,
            "clipboard": clipboard_match.group(1).strip() if clipboard_match else None,
        }

    def export(self):
        return {"messages": self.messages}
