#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mstranslator import Translator

from config import config

client_id = config.get('microsoft', 'client_id')
client_secret = config.get('microsoft', 'client_secret')

def btranslate(text_message,langfrom,langto):

  translator = Translator(client_id, client_secret)
  phrase_translated = translator.translate(text_message, lang_from=langfrom, lang_to=langto)
  #print phrase_translated
  return phrase_translated.encode('utf8')
