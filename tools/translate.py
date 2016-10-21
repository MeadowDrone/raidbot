#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shlex

from mstranslator import Translator
from config import config


def translate(text):
    text = text.replace('/translate', '').encode('utf-8')

    if '"' in text:
        noquotes = False
    else:
        noquotes = True

    message_broken = shlex.split(text)
    error = "not enough parameters. use /translate en hi \"hello world\" or /translate help"

    if not len(message_broken) < 1:
        if message_broken[0] == 'help':
            help_string = """ usage: /translate en hi "Hello world" (note the speech marks for phrases)\nlanguages:
                    ar-Arabic | bs-Latn-Bosnian (Latin) | bg-Bulgarian | ca-Catalan | zh-CHS-Chinese Simplified |
                    zh-CHT-Chinese Traditional|hr-Croatian | cs-Czech | da-Danish | nl-Dutch |en-English | cy-Welsh |
                    et-Estonian | fi-Finnish | fr-French | de-German | el-Greek | ht-Haitian Creole | he-Hebrew |
                    hi-Hindi | mww-Hmong Daw | hu-Hungarian | id-Indonesian | it-Italian | ja-Japanese | tlh-Klingon |
                    tlh - Qaak-Klingon (pIqaD) | ko-Korean | lv-Latvian | lt-Lithuanian | ms-Malay | mt-Maltese |
                    no-Norwegian | fa-Persian | pl-Polish | pt-Portuguese | otq-Queretaro Otomi | ro-Romanian |
                    ru-Russian | sr-Cyrl-Serbian (Cyrillic) | sr-Latn-Serbian (Latin) | sk-Slovak | sl-Slovenian |
                    es-Spanish | sv-Swedish | th-Thai | tr-Turkish | uk-Ukrainian | ur-Urdu | vi-Vietnamese |
                    """
            return help_string
        else:
            if len(message_broken) < 3:
                return error
            else:
                lang_from = message_broken[0]
                lang_to = message_broken[1]
                lang_text = message_broken[2]

                if noquotes:
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=btranslate(lang_text, lang_from, lang_to) +
                        "\n(note: use quotes around phrase for whole phrases, eg. /translate en it \"hello world\")")
                else:
                    return btranslate(lang_text, lang_from, lang_to)
    else:
        return error


def btranslate(text_message, langfrom, langto):
    client_id = config.get('microsoft', 'client_id')
    client_secret = config.get('microsoft', 'client_secret')

    translator = Translator(client_id, client_secret)
    phrase_translated = translator.translate(
        text_message, lang_from=langfrom, lang_to=langto)

    return phrase_translated.encode('utf8')
