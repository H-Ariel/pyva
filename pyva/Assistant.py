import webbrowser
import os
import datetime
import smtplib
import pyjokes

import AssistantAI
import AssistantIO
import LoginDataManager
import consts
import LogFile
from DoNotUnderstandException import DoNotUnderstandException


class Assistant:
	'''
	The assistant
	'''

	def __init__(self):
		''' init the assistant '''
	
		INTENT_METHODS = {
			'no tag'          : Assistant.no_tag,
			'goodbye'         : Assistant.goodbye,
			'about'           : Assistant.about,
			
			'send mail'       : Assistant.send_mail,
			'write note'      : Assistant.write_note,
			'show note'       : Assistant.show_notes,
			'change password' : Assistant.change_password,

			'tell joke'       : Assistant.tell_joke,
			'show time'       : Assistant.show_time,
			'show date'       : Assistant.show_date,

			'open mail'       : Assistant.open_mail,
			'open news'       : Assistant.open_news,
			'open google'     : Assistant.open_google,
			'open youtube'    : Assistant.open_youtube,
			'open weather'    : Assistant.open_weather
		}

		self.ai = AssistantAI.AssistantAI(INTENT_METHODS)
		self.io = AssistantIO.AssistantIO()
	
		self.run = True

		self.speak(f'Hello {LoginDataManager.USERNAME}')
		self.speak(f"I'm {consts.NAME}")
		self.speak('How can I Help you?')
	

	def speak(self, text):
		return self.io.speak(text)

	def get_input(self, text = ''):
		return self.io.get_input(text)
	

	def parse_message(self, msg):
		msg = msg.lstrip()
		if msg == '': return
		msg = msg.lower()
	
		json_log = None
		
		if self.try_parse_witout_ai(msg):
			json_log = { 'message': msg, 'result': 'not AI' }
		else:
			try:
				self.speak(self.ai.parse_message(msg, self))
			except DoNotUnderstandException:
				self.speak("I don't understand.")
				json_log = { 'message': msg, 'result': 'DoNotUnderstandException' }

		if json_log is not None:
			LogFile.write_json(json_log)

	
	# FUNCTIONS #

	def try_parse_witout_ai(self, msg):
		''' If successful - returns True, else - False '''

		if msg.startswith('open'):
			path = msg[4:].lstrip() # 4 == len('open')
			if path == '':
				path = self.get_input('What should I open?')
			
			try:
				os.startfile(path)
				return True
			except FileNotFoundError:
				#print(f'Error: No such file or directory: "{path}"')
				return False

		elif msg.startswith('search '):
			webbrowser.open('https://google.com/search?q=' + msg[6:].lstrip()) # 6 == len('search')
			return True

		return False


	def no_tag(self):
		#self.speak("I don't understand.")
		raise DoNotUnderstandException()
	

	def goodbye(self):
		self.run = False
	

	def about(self):
		self.speak(f"I'm {consts.NAME}")
		self.speak("I created by Ariel in April 2022")
		self.speak("It's important to me that you know I'm always here for you")
	

	def send_mail(self):
		# TODO: Enable low security in gmail
	
		try:
			self.speak('To whom to send it? Please write the email address here')
			to = input()
			content = self.get_input('What should I say? ')
			
			with smtplib.SMTP('smtp.gmail.com', 587) as server:
				server.ehlo()
				server.starttls()
				server.login('danip89687@gmail.com', '2v4a+DvJ%@')
				server.sendmail('danip89687@gmail.com', to, content)
	
			self.speak('\nThe email was sent successfully')
	
		except Exception as e:
			print('Error:', e)
			self.speak('I am not able to send this email')
	

	def write_note(self):
		note = self.get_input('What should I write?')
		with open(consts.NOTES_FILE_PATH, 'a') as file:
			file.write(note + '\n')
		
		self.speak('The note was written successfully')
	

	def show_notes(self):
		if os.path.exists(consts.NOTES_FILE_PATH):
			self.speak('Showing Notes')
			with open(consts.NOTES_FILE_PATH, 'r') as file:
				for line in file:
					print(line, end='')
		else:
			self.speak('You have not made any notes yet')
	

	def change_password(self):
		self.speak('Look in console')
		LoginDataManager.set_login_data_from_user()
		self.speak('The change was successful')


	def tell_joke   (self): self.speak(pyjokes.get_joke(category='all'))
	def show_time   (self): self.speak('The current time is ' + datetime.datetime.now().strftime('%H:%M'))
	def show_date   (self): self.speak('The current date is ' + datetime.datetime.now().strftime('%A, %B %e %Y'))
	def open_mail   (self): webbrowser.open('https://mail.google.com/mail/u/0/#inbox')
	def open_news   (self): webbrowser.open('https://news.google.com/topstories')
	def open_google (self): webbrowser.open('https://google.com/')
	def open_youtube(self): webbrowser.open('https://youtube.com/')
	def open_weather(self): webbrowser.open('https://weather.com/')
