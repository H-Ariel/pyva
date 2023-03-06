import getpass
import hashlib


LOGIN_DATA_FILE = 'login_data.dat'
USERNAME = 'Ariel'


def get_md5(msg: str):
	return hashlib.md5(msg.encode()).hexdigest()


def get_login_data():
	try:
		with open(LOGIN_DATA_FILE, 'r') as f:
			return f.read().split(' ')
	
	except Exception:
		return get_md5(USERNAME), get_md5('')


def set_login_data(new_username, new_password):
	with open(LOGIN_DATA_FILE, 'w') as f:
		f.write(get_md5(new_username) + ' ' + get_md5(new_password))


def set_login_data_from_user():
	if try_login(True):
		new_username = input('New Username: ')
		new_password = getpass.getpass('New Password: ')
		set_login_data(new_username, new_password)


def try_login(old=False):
	'''
	Try to login. If successful - returns True, else - False
	if `old` parameter is `True` it will write 'Old Username' and 'Old Password'
	'''

	valid_login_data = get_login_data()

	username = input(('Old ' if old else '') + 'Username: ')
	password = getpass.getpass(('Old ' if old else '') + 'Password: ')

	if (get_md5(username), get_md5(password)) != valid_login_data:
		print('Incorrect login data')
		return False

	global USERNAME
	USERNAME = username

	return True
