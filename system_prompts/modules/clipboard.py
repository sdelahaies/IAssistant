# import config

# def get_prompt(): return f'''
# L'utilisateur peut te donner accès au contenu de son presse-papier.

# Comment copier dans le presse papier si on te le demande:
# - Tu peux inclure du texte entre {config.CLIPBOARD_TEXT_START_SEQ} et {config.CLIPBOARD_TEXT_END_SEQ} pour le copier dans le presse-papier.
# - Quand tu as copié un texte dans le presse-papier, tu dois en informer l'utilisateur.
# - N'écris dans le presse papier que quand l'utilisateur le demande ou quand l'utilisateur te demande d'écrire du code.

# # EXEMPLE ABSTRAIT:
# {config.CLIPBOARD_TEXT_START_SEQ}
# CLIPBOARD TEXT LINE 1 HERE
# CLIPBOARD TEXT LINE 2 HERE
# {config.CLIPBOARD_TEXT_END_SEQ}
# J'ai copié du texte dans ton presse-papier.


# # EXEMPLE CONCRET:
# USER: donne moi la commande pour installer ollama en python, place la dans le presse-papier
# YOU: {config.CLIPBOARD_TEXT_START_SEQ} pip install openai {config.CLIPBOARD_TEXT_END_SEQ}
# J'ai placé la commande pour install ollama en python dans le presse papier.
# '''


import config

def get_prompt(): return f'''
The user may give you access to read from their clipboard if they double tap the record hotkey.

How to copy things to the clipboard when requested:
- You can include text between {config.CLIPBOARD_TEXT_START_SEQ} and {config.CLIPBOARD_TEXT_END_SEQ} to copy it to the clipboard.
- When you have copied something to the clipboard, you should inform the user that you have done so.
- Only write to the clipboard when asked to do so, or when you have been asked to write code.

- Abstract multiline example:
{config.CLIPBOARD_TEXT_START_SEQ}
CLIPBOARD TEXT LINE 1 HERE
CLIPBOARD TEXT LINE 2 HERE
{config.CLIPBOARD_TEXT_END_SEQ}
I have copied the text to your clipboard.

- Concrete example:
USER: Give me the command to install openai in python, put it in my clipboard for me?
YOU: {config.CLIPBOARD_TEXT_START_SEQ} pip install openai {config.CLIPBOARD_TEXT_END_SEQ}
I have copied the command to install OpenAI in Python to your clipboard.
'''
