import json

import consts


def write_text(text, new_line=True):
	with open(consts.LOG_FILE, 'a') as log_file:
		log_file.write(text)
		if new_line:
			log_file.write('\n')

def write_json(json_obj, new_line=True):
	#write_text(json.dumps(json_obj, indent=2), new_line)
	write_text(json.dumps(json_obj), new_line)
