# IAssistant: An Adaptable AI Voice Assistant

IAssistant is a demo project to start with a customizable AI voice assistant. It is build by adapting the core functionalities of the [AlwaysReddy](https://github.com/ILikeAI/AlwaysReddy) project. AlwaysReddy is designed for multi-OS environments, with a couple of clients to choose from, it simplifies a variety of tasks through speech and text-based interaction, featuring enhanced extensibility and user-friendly controls via a terminal based app with hotkeys controls. 

IAssistant is meant for linux, Windows and Mac stuff has been striped out, remote AI clients have been removed as well to prefer opensource local tools but hence requires a GPU with sufficient VRAM to allow for small latency.

**Disclaimer:** This project is a starter project, currently under construction. It provides basic logic and simple use cases, far from perfect and subject to occasional bugs. Have you ever received an awkward answer from an LLM due to a messy prompt? Imagine when your assistant speaks it out loud! While it’s a fun and half-functional demonstration, it’s still a work in progress—designed to explore possibilities, not polished for production by any means. Use with curiosity and a pinch of patience! 😅 

## Features

- **Clipboard Integration**: Leverages clipboard content for completing tasks based on user requests.
- **PDF Handling**: Enables querying and interaction with content in PDF documents.
- **Customizable Components**:
  - Transcriber engine: Use [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) or [OpenAI Whisper](https://huggingface.co/openai/whisper-large-v3-turbo).
  - Transcriber model: Choose from available models like `openai/whisper-large-v3-turbo`, `tiny.en`, etc.
  - LLM: Integrate any compatible LLM via [Ollama](https://ollama.com/) with adaptable prompts.
  - System prompts: Tailor prompts to suit specific use cases.
  - Text-to-speech voice: Utilize [Piper](https://github.com/rhasspy/piper/tree/master) to set the desired voice.
- **Speech Output**: Conversational answers are spoken aloud.
- **Clipboard Outputs**: Outputs formatted text or code directly to the clipboard for further use.
- **Python GTK Interface**: A graphical interface replaces terminal-based logic, enabling intuitive settings adjustment (e.g., model, voice, prompt).

## Installation

Ensure your environment is set up for Python-based AI development tasks. Then, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/sdelahaies/IAssistant.git
   cd IAssistant
   ```

2. Install the assistant using the setup script:
   ```bash
   python setup.py
   ```

3. Start the assistant:
   ```bash
   ./run_IAssistant.sh
   ```

# install voices

A default english voice is present in the repo `piper_tss/voices/voice_en_1/`, download other voices [here](https://rhasspy.github.io/piper-samples/), place them in `piper_tss/voices/` and update `voice_list` in `main.py`. 


## TODO

- [x] update system prompts
- [ ] allow for the use of uv instead of virtualenv
- [ ] add specific use cases
- [ ] keep up cleaning up the repo!
- [ ] **Vision Model Integration**: Enable handling of images copied to the clipboard for document-related queries.
- [ ] **Image Generation**: Add functionality to generate images using diffuser models (e.g., [Stable Diffusion XL](https://stability.ai/)).

## References

- [Using AI to Solve Real-World Problems](https://github.com/sdelahaies/IAssistant)
- [AlwaysReddy: Terminal-based AI Assistant](https://github.com/ILikeAI/AlwaysReddy)
- [Ollama: Get up and running with large language models](https://ollama.com/)
- [OpenAI Whisper Large v3 Turbo](https://huggingface.co/openai/whisper-large-v3-turbo)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [Piper: Neural Text-to-Speech](https://github.com/rhasspy/piper/tree/master)
- [The Python GTK+ 3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/)
- [Need to logo for your app? Check out this huggingface space](https://huggingface.co/spaces/fantaxy/ofai-flx-logo) Prompt: [Style: Minimalist] [Color: black and White] [Concept: AI] [Text: 'IA'] [Background: circular vortex]


