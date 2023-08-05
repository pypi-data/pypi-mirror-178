#!./runmodule.sh

'''
Config Attributes

A python library to read and write config files
with a syntax inspired by vimrc and ranger config.
'''

__version__ = '0.3.3'

from .config import *
from .configfile import *

__all__ = [
	# -------- user interface -------
	# imported from config
	'Config',
	'DictConfig',
	'ConfigTrackingChanges',
	'MultiConfig',
	'MultiDictConfig',
	'ConfigId',
	# imported from configfile
	'ConfigFile',
	'NotificationLevel',
	# -------- internals -------
	# imported from config
	'InstanceSpecificDictMultiConfig',
	# imported from configfile
	'readable_quote',
	'UiCallback',
	'ParseException',
	'MultipleParseExceptions',
]
