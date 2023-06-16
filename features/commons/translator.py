from deep_translator import MyMemoryTranslator



def translate_scraped(title, desc, from_len = "en", to_len = "fr"):

    title = MyMemoryTranslator(source=from_len, target=to_len).translate(title)
    desc = MyMemoryTranslator(source=from_len, target=to_len).translate(desc)

    return title, desc
