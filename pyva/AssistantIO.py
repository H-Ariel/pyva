import pyttsx3
import speech_recognition as sr

import consts


class AssistantIO:
	'''
	The input/output manager of the assistant
	'''

	if consts.IO_TYPE == consts.IOTypes.TEXT:
		def speak(self, text):
			print(text)

		def get_input(self, text = ''):
			return input(text + '\n=> ')

	else:
		def __init__(self):
			self.engine = pyttsx3.init('sapi5')
			self.engine.setProperty('voice', self.engine.getProperty('voices')[consts.IO_TYPE.value].id)
			self.recognizer = sr.Recognizer()

		def speak(self, text):
			print(text)		
			self.engine.say(text)
			self.engine.runAndWait()
	
		def get_input(self, text = ''):
			self.speak(text)	
	
			with sr.Microphone() as Microphone:
				print('Listening...')
				audio = self.recognizer.listen(Microphone)
		
			try:
				print('Recognizing...')
				query = self.recognizer.recognize_google(audio, language='en-US')
				print('=>', query)
			except sr.UnknownValueError:
				self.speak('Say that again, please...')
				return ''
			except sr.RequestError:
				self.speak("Error: Couldn't request results from Google Speech Recognition service")
				return ''
		
			return query
