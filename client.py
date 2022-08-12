import slixmpp
import time
import json
from aioconsole import ainput, aprint
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
	def __init__(self, jid, password, algorithm):
		slixmpp.ClientXMPP.__init__(self, jid, password)
		self.algorithm = algorithm
		
		data_file = input('Enter the file for information:\n>>')
		# READ JSON FILE FOR FLOODING
		f = open(data_file)
		algorithm_data = json.load(f)
		print(algorithm_data)

		# listeners
		self.add_event_handler("session_start", self.start)
		self.add_event_handler('message', self.message)

		# plugins
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0199') # Ping
		self.register_plugin('xep_0004') # Data Forms
		self.register_plugin('xep_0060') # PubSub
		self.register_plugin('xep_0199') # XMPP Ping


	async def start(self, event):
		try:
			self.send_presence()
			await self.get_roster()
			# TODO: add menu to send messages
			connected = True
			while connected:
				await aprint("""
				1. Send message\n
				2. Exit\n
				""")
				option = await ainput('>> ')
				if option == '1':
					jid_to = await ainput('JID to: ')
					message = await ainput('Message: ')
					self.send_message(
						mto=jid_to,
						mbody=message,
						mtype='chat'
					)
				elif option == '2':
					connected = False
					self.disconnect()
				else:
					await aprint('Invalid option')
					time.sleep(1)
		except IqError as err:
			aprint(f"Error: {err.iq['error']['text']}")
			self.disconnect()
		except IqTimeout:
			aprint('Error: Server is taking too long to respond')
			self.disconnect()
	
	def message(self, msg):
		print('message', msg)
		if msg['type'] in ('normal', 'chat'):
			aprint(msg['body'])
