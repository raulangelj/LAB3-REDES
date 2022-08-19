import time
import logging
import asyncio
from client import Client
from optparse import OptionParser

first_menu = """
1. Log in\n
2. Choose a algorithm\n
3. Load information file\n
4. Exit\n"""

algorithm_menu = """
1. Flooding\n
2. Distance vector routing\n
3. Link state routing\n
4. Exit\n
"""

if __name__ == '__main__':
	optp = OptionParser()
	optp.add_option('-d', '--debug', help='set loggin to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
	opts, args = optp.parse_args()

	# ! DO NOT DELETE THIS LINE, PATCH A ERROR ON ASYNCIO LIB
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

	logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

	print('======= LAB 3 =======')
	option = 0
	print(algorithm_menu)
	algorithm = input('Choose an algorithm:\n>>')
	if algorithm == '1':
		print('Flooding')
		jid = input('Enter your JID: (without @alumchat.fun) \n>>')
		password = input('Enter your password: \n>>')
		jid = f'{jid}@alumchat.fun'
		client = Client(jid, password, 'flooding')
		client.connect(disable_starttls=False)
		client.process(forever=False)
		exit(1)
	elif algorithm == '2':
		print('Distance vector routing')
	elif algorithm == '3':
		print('Link state routing')
	elif algorithm == '4':
		print('Exit')
		exit(1)
	else:
		print('Invalid option')
		time.sleep(1)
	# while option != '4':
	# 	print(first_menu)
	# 	option = input('Choose an option:\n> ')
	# 	if option == '1':
	# 		jid = input('JID: ')
	# 		password = input('Password: ')
	# 		client = Client(jid, password)
	# 		client.connect(disable_starttls=False)
	# 		client.process()
	# 	elif option == '2':
	# 		pass
	# 	elif option == '3':
	# 		pass
	# 	elif option == '4':
	# 		print('Goodbye!')
	# 	else:
	# 		print('Invalid option')
	# 		time.sleep(1)
	# 		continue
