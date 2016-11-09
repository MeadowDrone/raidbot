from tools.static_config import static_config

def quote(term):
    names = static_config.get('static', 'names')
    return names
