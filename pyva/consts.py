'''
This module contains constant variables for the program.
'''


import enum


class IOTypes(enum.Enum):
	'''
	The type of way you communicate with the assistant
	Used in class AssistantIO
	'''

	MALE_VOICE   = 0
	FEMALE_VOICE = 1
	TEXT = 2


IO_TYPE = IOTypes.TEXT
NAME = 'Pyva' # Python Virtual Assistant


PYVA_ROOT_DIRECTORY = 'pyva-files/'

INTENTS_FILE = f'{PYVA_ROOT_DIRECTORY}intents.json'
MODEL_NAME   = f'{PYVA_ROOT_DIRECTORY}SavedModel/pyva-model'
LOG_FILE     = f'{PYVA_ROOT_DIRECTORY}log.log'
NOTES_FILE_PATH = f'{PYVA_ROOT_DIRECTORY}notes.dat'
