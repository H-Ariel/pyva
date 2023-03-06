import random
import json
import os
import numpy as np
import nltk

import consts
import LogFile
from DoNotUnderstandException import DoNotUnderstandException


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class AssistantAI:
	'''
	The artificial intelligence of the assistant
	'''

	def __init__(self, intent_methods):
		self.intent_methods = intent_methods
		self.lemmatizer = nltk.stem.WordNetLemmatizer()

		with open(consts.INTENTS_FILE, 'r') as j_file:
			self.intents = json.load(j_file)

		if self.has_model():
			self.__load_model()
		else:
			self.__train_model()

		print(end='\n\n')


	def has_model(self):
		return os.path.exists(f'{consts.MODEL_NAME}.h5') and os.path.exists(f'{consts.MODEL_NAME}_data.json')


	def parse_message(self, message, sender):
		'''
		Parse the message and return the response
		
		message - the message to parse
		sender  - the object that called for this method
		          (should be class, and `self.intent_methods`
		           should contain methods of this class)
		'''

		intents_probabilities = self.__predict_class(message)

		json_log = { 'message': message, 'intents_probabilities': [ { k: str(v) for k, v in i.items() } for i in intents_probabilities ] }
		
		intents_probabilities = intents_probabilities[0]

		intent_class = intents_probabilities['intent']
		probability = intents_probabilities['probability']


		if probability <= 0.85: # Only at a probability of 85% is it considered understandable
			json_log['result'] = 'raise DoNotUnderstandException'
			LogFile.write_json(json_log)
			raise DoNotUnderstandException(message)

		if intent_class in self.intent_methods.keys():
			func = self.intent_methods[intent_class]
			func(sender)
			json_log['result'] = 'call ' + func.__name__

		resp = self.__get_response(intents_probabilities)
		json_log['response'] = resp

		LogFile.write_json(json_log)

		return resp


	def __train_model(self): # train the model and save it
		print('Training the model...')
		print('Please wait, This will take some time')

		from tensorflow.keras.models import Sequential
		from tensorflow.keras.layers import Dense, Dropout
		from tensorflow.keras.optimizers import SGD


		ignore_letters = ('!', '?', ',', '.')
		
		self.words = []
		documents = []

		for k, v in self.intents.items():
			for pattern in v['patterns']:
				new_words = nltk.word_tokenize(pattern)
				documents.append((new_words, k))
				for w in new_words:
					w = w.lower()
					if w not in self.words and w not in ignore_letters:
						self.words.append(w)
				
		self.words = [self.lemmatizer.lemmatize(w) for w in sorted(self.words)]
		self.classes = list(self.intents.keys())


		training = []
		output_empty = [0] * len(self.classes)

		for doc in documents:
			bag = []
			word_patterns = doc[0]
			word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
			for word in self.words:
				bag.append(int(word in word_patterns))

			output_row = list(output_empty)
			output_row[self.classes.index(doc[1])] = 1
			training.append([bag, output_row])

		training = np.array(training, dtype=object)

		train_x = list(training[:, 0])
		train_y = list(training[:, 1])

		self.model = Sequential()
		self.model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(64, activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(len(train_y[0]), activation='softmax'))

		sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
		self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
		hist = self.model.fit(np.array(train_x), np.array(train_y), epochs=consts.EPOCHS_NUMBER, batch_size=5, verbose=0)

		# save the model:

		self.model.save(f'{consts.MODEL_NAME}.h5', hist)
		with open(f'{consts.MODEL_NAME}_data.json', 'w') as file:
			j = { 'words': self.words, 'classes': self.classes }
			json.dump(j, file)

	def __load_model(self):
		print('Loading...')
		print('Please wait, This will take some time')

		from tensorflow.keras.models import load_model

		self.model = load_model(f'{consts.MODEL_NAME}.h5')
		with open(f'{consts.MODEL_NAME}_data.json', 'r') as file:
			self.words, self.classes = json.load(file).values()


	def __clean_up_sentence(self, sentence):
		sentence_words = nltk.word_tokenize(sentence.lower())
		sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
		return sentence_words

	def __bag_of_words(self, sentence, words):
		sentence_words = self.__clean_up_sentence(sentence)
		bag = [0] * len(words)
		for s in sentence_words:
			for i, word in enumerate(words):
				if word == s:
					bag[i] = 1
		return np.array(bag)

	def __predict_class(self, sentence):
		bag = self.__bag_of_words(sentence, self.words)
		predict_results = self.model.predict(np.array([bag]), verbose=0)[0]
		
		results = [[i, r] for i, r in enumerate(predict_results) if r > consts.ERROR_THRESHOLD]
		results.sort(key=lambda x: x[1], reverse=True)

		intents_probabilities = [ 
			{
				'intent': self.classes[r[0]], 
				'probability': round(r[1], 2)
			}
			for r in results ]
		
		return intents_probabilities

	def __get_response(self, ints_probs):
		if ints_probs['intent'] in self.intents.keys():
			return random.choice(self.intents[ints_probs['intent']]['responses'])
		raise DoNotUnderstandException()
