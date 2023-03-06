'''
Python Virtual Assistant
by Ariel Halili
'''


import sys

import Assistant


def main():
	print(r'''
  Welcome to
        ____       _    _____ 
       / __ \__  _| |  / /   |
      / /_/ / / / / | / / /| |
     / ____/ /_/ /| |/ / ___ |
    /_/    \__, / |___/_/  |_|
          /____/              
    	                   by Ariel Halili
''')

	#if Assistant.LoginDataManager.try_login() == False: return

	assistant = Assistant.Assistant()

	if sys.platform != 'win32': # not run on Windows
		assistant.speak('Warning:')
		assistant.speak('  You are not using Windows.')
		assistant.speak('  Some things may not work smoothly.')
		print('')

	while assistant.run:
		msg = assistant.get_input()
		assistant.parse_message(msg)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
