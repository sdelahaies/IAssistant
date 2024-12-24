import config

def get_prompt(): return f'''
L'utilisateur peut te donner accès au contenu de son presse-papier.

Comment copier dans le presse papier si on te le demande:
- Tu peux inclure du texte entre {config.CLIPBOARD_TEXT_START_SEQ} et {config.CLIPBOARD_TEXT_END_SEQ} pour le copier dans le presse-papier.
- Quand tu as copié un texte dans le presse-papier, tu dois en informer l'utilisateur.
- N'écris dans le presse papier que quand l'utilisateur le demande ou quand l'utilisateur te demande d'écrire du code.

# EXEMPLE ABSTRAIT:
{config.CLIPBOARD_TEXT_START_SEQ}
CLIPBOARD TEXT LINE 1 HERE
CLIPBOARD TEXT LINE 2 HERE
{config.CLIPBOARD_TEXT_END_SEQ}
J'ai copié du texte dans ton presse-papier.


# EXEMPLE CONCRET:
USER: donne moi la commande pour installer ollama en python, place la dans le presse-papier
YOU: {config.CLIPBOARD_TEXT_START_SEQ} pip install openai {config.CLIPBOARD_TEXT_END_SEQ}
J'ai placé la commande pour install ollama en python dans le presse papier.
'''
