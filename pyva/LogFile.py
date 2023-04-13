import consts


def write_text(text, new_line=True):
	with open(consts.LOG_FILE, 'a') as log_file:
		log_file.write(text)
		if new_line:
			log_file.write('\n')

def write_json(json_obj, new_line=True):
	txt = ''
	for k, v in json_obj.items():
		txt += f'{k}: {v}\t'
	txt = txt[:-1]
	write_text(txt, new_line)
