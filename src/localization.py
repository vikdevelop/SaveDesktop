import json
import locale
import os

# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
elif 'zh' in p_lang:
    r_lang = 'zh_Hans'
else:
    r_lang = p_lang[:-3]

flatpak = os.path.exists("/.flatpak-info")
if flatpak:
  try:
      locale = open(f"/app/translations/{r_lang}.json")
  except:
      locale = open(f"/app/translations/en.json")
else:
  # Check if the detected language is exists in the app language list
  try:
      locale = open(f"translations/{r_lang}.json")
  except:
      locale = open("translations/en.json")

_ = json.load(locale)
