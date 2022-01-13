import configparser
from pathlib import Path
import os
from .main import write_to_file

default_location = input('Default project location (~/git, etc.): ')

config_file = Path.expanduser(Path('~/flask_gen.config'))

config = configparser.ConfigParser()
config.read('FILE.INI')
print(config['DEFAULT']['path'])     # -> "/path/name/"
config['DEFAULT']['path'] = '/var/shared/'    # update
config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

with open('FILE.INI', 'w') as configfile:    # save
    config.write(configfile)


