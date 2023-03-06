'''
This program generate a JSON file to train the model
'''

intents = { 
	"no tag":{
		"patterns": [ "" ],
		"responses": [ "" ]
	},
	"greeting":
	{
		"patterns": [
			"Hi",
			"Hey",
			"Hello"
		],
		"responses": [
			"Hello!",
			"Good to see you again!",
			"Hi there, how can I help?"
		]
	},
	"goodbye":
	{
		"patterns": [
			"See you later",
			"Goodbye",
			"I am Leaving",
			"bye",
			"exit",
			"quit"
		],
		"responses": [
			"Sad to see you go :(",
			"See you later",
			"Goodbye!"
		]
	},
	"thanks":
	{
		"patterns": [
			"thanks",
			"thanks you",
			"thank you",
			"thank you so much"
		],
		"responses": [
			"glad to help you",
			"you're welcome",
			"always at your service"
		]
	},
	"<emotion question>":
	{
		"patterns": [
			"how are you",
			"how are you today",
			"How was your day"
		],
		"responses": [
			"I'm fine, glad you're here",
			"Today I feel great"
		]
	},
	"about":
	{
		"patterns": [
			"what is your name",
			"what's your name",
			"who are you",
			"what are you",
			"who made you",
			"who created you",
			"tell me about your",
			"tell me about yourself"
		],
		"responses": [ "" ]
	},
	"tell joke":
	{
		"patterns": [
			"tell me a joke",
			"tell me joke",
			"tell joke"
		],
		"responses": [ "" ]
	},
	"send mail":
	{
		"patterns": [
			"send mail",
			"send a mail",
			"send email",
			"send an email"
		],
		"responses": [ "" ]
	},
	"change password":
	{
		"patterns": [
			"change password",
			"change the password",
			"set password",
			"set new password",
			"set another password"
		],
		"responses": [ "" ]
	}
}


def get_all_combinations(l1, l2):
	return [i + ' ' + j for i in l1 for j in l2]

def add_intent(tag, patterns, responses = [""]):
	intents[tag] = { 'patterns': patterns, 'responses': responses }

def add_date_and_time():
	words = [ "what is the", "what's the", "show current", "display current" ]
	add_intent("show time", get_all_combinations(words, ['time']))
	add_intent("show date", get_all_combinations(words, ['date']))

def add_write_notes():
	l1 = ['write', 'save', 'remember']
	l2 = ['note', 'notes']
	add_intent('write note', get_all_combinations(l1, l2))

def add_read_notes():
	l1 = ['show', 'display', 'open', 'read']
	l2 = ['note', 'notes']
	add_intent('show note', get_all_combinations(l1, l2))

def add_open_sites():
	add_intent('open mail', get_all_combinations(['open'], ['mail', 'gmail']))
	add_intent('open news', get_all_combinations(['open'], ['news']))
	add_intent('open google', get_all_combinations(['open'], ['google']))
	add_intent('open youtube', get_all_combinations(['open'], ['youtube']))
	add_intent('open weather', get_all_combinations(['open', 'what is', "what's"], ['weather']))


def generate_json():
	add_date_and_time()
	add_write_notes()
	add_read_notes()
	add_open_sites()

	import json
	with open('new_intents.json', 'w') as f:
		f.write(json.dumps(intents, indent=2))


if __name__ == '__main__':
	generate_json()
