import os
import configparser

config = configparser.ConfigParser()
confile = os.path.join(os.path.dirname(__file__), '../data', 'config.ini')
config.read(confile)