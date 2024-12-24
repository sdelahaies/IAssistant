import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from soundfx import play_sound_FX

from IAssistant import IAssistant

from ollama import chat
from ollama import ChatResponse

from pprint import pprint
from datetime import datetime
import json

import threading

import clipboard

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

IA = IAssistant()
IA.init_recoder()
IA.init_transcriber()
IA.init_tts()

volume = 0.5

model_list = ["llama3.2:3b"]
prompt_list = ["default_prompt_en", "default_prompt_fr"]
voice_list = ["voice_en_1", "voice_en_2", "voice_fr_1", "voice_fr_2"]
transcriber_list = ["TransformersWhisper", "FasterWhisper"]
transcriber_model_list = [
    "tiny.en",
    "Philogicae/whisper-large-v3-french-ct2",
    "ammaraldirawi/faster-whisper-small-fr-int8",
]


class IAssistantWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="IAssistant")
        self.set_icon_from_file("favicon.ico")
        self.set_border_width(10)
        self.set_default_size(300, 250)

        # Create a vertical box to organize widgets
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_homogeneous(False)
        self.add(self.vbox)

        self.settings_label = Gtk.Label(label="Settings")
        self.settings_label.set_alignment(0, 0.5)
        self.apply_button = Gtk.Button(label="Apply")
        self.apply_button.connect("clicked", self.on_apply_clicked)
        settings_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        settings_row.set_homogeneous(False)
        settings_row.pack_start(self.settings_label, True, True, 0)
        settings_row.pack_start(self.apply_button, True, True, 0)
        self.vbox.pack_start(settings_row, True, True, 0)

        # Transcriber row
        self.transcriber_label = Gtk.Label(label="Transcriber")
        self.transcriber_label.set_alignment(0, 0.5)
        self.transcriber_combo = Gtk.ComboBoxText()
        for transcriber_name in transcriber_list:
            self.transcriber_combo.append_text(transcriber_name)
        self.transcriber_combo.set_active(0)
        transcriber_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        transcriber_row.set_homogeneous(False)
        transcriber_row.pack_start(self.transcriber_label, True, True, 0)
        transcriber_row.pack_start(self.transcriber_combo, True, True, 0)
        self.vbox.pack_start(transcriber_row, True, True, 0)

        # LLM row
        self.llm_label = Gtk.Label(label="Model")
        self.llm_label.set_alignment(0, 0.5)
        self.llm_combo = Gtk.ComboBoxText()
        for model_name in model_list:
            self.llm_combo.append_text(model_name)
        self.llm_combo.set_active(0)
        llm_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        llm_row.set_homogeneous(False)
        llm_row.pack_start(self.llm_label, True, True, 0)
        llm_row.pack_start(self.llm_combo, True, True, 0)
        self.vbox.pack_start(llm_row, True, True, 0)

        # piper row
        self.piper_label = Gtk.Label(label="Piper")
        self.piper_label.set_alignment(0, 0.5)
        self.piper_combo = Gtk.ComboBoxText()
        for voice_name in voice_list:
            self.piper_combo.append_text(voice_name)
        self.piper_combo.set_active(0)
        piper_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        piper_row.set_homogeneous(False)
        piper_row.pack_start(self.piper_label, True, True, 0)
        piper_row.pack_start(self.piper_combo, True, True, 0)
        self.vbox.pack_start(piper_row, True, True, 0)

        self.prompt_label = Gtk.Label(label="System prompt")

        # piper row
        self.prompt_label = Gtk.Label(label="System prompt")
        self.prompt_label.set_alignment(0, 0.5)
        self.prompt_combo = Gtk.ComboBoxText()
        for prompt in prompt_list:
            self.prompt_combo.append_text(prompt)
        self.prompt_combo.set_active(0)
        prompt_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        prompt_row.set_homogeneous(False)
        prompt_row.pack_start(self.prompt_label, True, True, 0)
        prompt_row.pack_start(self.prompt_combo, True, True, 0)
        self.vbox.pack_start(prompt_row, True, True, 0)

        self.record_button = Gtk.Button(label="●")
        self.record_button.set_name("record_button")
        self.record_button.get_style_context().add_class("green-button")
        self.record_button.connect("clicked", self.on_record_button_clicked)
        self.vbox.pack_start(self.record_button, False, False, 0)

        self.clear_clipboard_button = Gtk.Button(label="Clear clipboard")
        self.vbox.pack_start(self.clear_clipboard_button, False, False, 0)

        self.export_button = Gtk.Button(label="Export")
        self.vbox.pack_start(self.export_button, False, False, 0)

        self.import_button = Gtk.Button(label="Import")
        self.vbox.pack_start(self.import_button, False, False, 0)

        self.new_button = Gtk.Button(label="New")
        self.vbox.pack_start(self.new_button, False, False, 0)

        # Connect signals to display apply button
        self.transcriber_combo.connect("changed", self.on_model_changed)
        self.llm_combo.connect("changed", self.on_model_changed)
        self.piper_combo.connect("changed", self.on_model_changed)

        self.export_button.connect("clicked", self.export)
        self.clear_clipboard_button.connect("clicked", self.clear_clipboard)

        # Style for the record button
        css = b"""
        .red-button {
            background-color: red;
            color: red;
            font-size: 25px;
        }
        .green-button {
            color: green;
            font-size: 25px;
        }
        .orange-button {
            color: orange;
            font-size: 25px;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        volumebutton = Gtk.VolumeButton()
        volumebutton.set_value(0.2)
        volumebutton.connect("value-changed", self.on_volume_button_changed)
        self.vbox.pack_start(volumebutton, False, False, 0)

    def clear_clipboard(self, button):
        clipboard.copy(None)

    def on_volume_button_changed(self, volumebutton, value):
        global volume
        volume = value
        print("VolumeButton value: %0.2f" % (volume))

    def on_model_changed(self, widget):
        if IA.transcriber_engine != self.transcriber_combo.get_active_text():
            self.apply_button.set_visible(True)
        if IA.tts_model != self.piper_combo.get_active_text():
            self.apply_button.set_visible(True)

    def on_apply_clicked(self, button):
        # Reload the interface or apply the settings
        print(f"Selected Transcriber: {self.transcriber_combo.get_active_text()}")
        print(f"Selected LLM: {self.llm_combo.get_active_text()}")
        if IA.transcriber_engine != self.transcriber_combo.get_active_text():
            IA.transcriber_engine = self.transcriber_combo.get_active_text()
            IA.init_transcriber()
        if IA.tts_model != self.piper_combo.get_active_text():
            IA.tts_model = self.piper_combo.get_active_text()
            IA.init_tts()
        self.apply_button.set_visible(False)

    def get_response(self):
        filename = "temp_recording.wav"
        transcript = IA.transcriber.transcribe_audio(filename)
        IA.set_prompt(transcript)
        response = IA.get_completion()
        print(response)
        IA.tts.run_tts(response, volume)

    def on_record_button_clicked(self, button):
        if "green-button" in button.get_style_context().list_classes():
            button.get_style_context().remove_class("green-button")
            button.get_style_context().add_class("red-button")
            play_sound_FX("start", volume=0.05, verbose=True)
            IA.recorder.start_recording()
            # self.record()
            # threading.Thread(target=self.simulate_api_stop_signal, args=(button,), daemon=True).start()
        else:
            button.get_style_context().remove_class("red-button")
            button.get_style_context().add_class("orange-button")
            IA.recorder.stop_recording()
            play_sound_FX("end", volume=0.05, verbose=True)
            threading.Thread(target=self.get_response, daemon=True).start()
            # self.get_response()
            button.get_style_context().remove_class("orange-button")
            button.get_style_context().add_class("green-button")

    def export(self, button):
        pprint(IA.export())
        with open(
            f"history_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", "w"
        ) as f:
            json.dump(IA.export(), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    app = IAssistantWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    app.apply_button.set_visible(False)
    Gtk.main()
