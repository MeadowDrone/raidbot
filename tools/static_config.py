import os
import configparser

static_config = configparser.ConfigParser()
static_confile = os.path.join(os.path.dirname(__file__), '../data', 'static_config.ini')
static_config.read(static_confile)
