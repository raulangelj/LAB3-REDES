import slixmpp
import time
import json
from LINK_STATE.dijkstra import Graph
from aioconsole import ainput, aprint
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
	def __init__(self, jid, password, algorithm):
		slixmpp.ClientXMPP.__init__(self, jid, password)
		self.algorithm = algorithm
		self.algorithm_data = {}

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
				await aprint(f"""
				(YOU ARE: {self.boundjid.bare})
				1. Send message\n
				2. Open file for algorithm\n
				3. Disconnect\n
				""")
				option = await ainput('>> ')
				if option == '1':
					if self.algorithm_data:
						jid_to = await ainput('JID to: ')
						message = await ainput('Message: ')
						await self.send_new_message(message, jid_to)
					else:
						print('You must open a file')
				elif option == '2':
					data_file = input('Enter the file for information:\n>>')
					# READ JSON FILE FOR FLOODING
					try:
						f = open(data_file)
						algorithm_data = json.load(f)
						self.algorithm_data = algorithm_data
						print(algorithm_data)
					except Exception as e:
						print(e)
				elif option == '3':
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
	
	async def message(self, message):
		user = str(message['from']).split('@')[0]
		await aprint(f'{user}: {message["body"]}')
		if self.algorithm == 'flooding':
			try:
				if not self.algorithm_data:
					# READ JSON FILE FOR FLOODING
					f = open('./FLOODING/flooding.json')
					algorithm_data = json.load(f)
					self.algorithm_data = algorithm_data
					print(algorithm_data)
				self.flooding(self.algorithm_data, message)
			except Exception as e:
				print(e)

	async def send_new_message(self, message, to):
		if self.algorithm == 'flooding':
			userName = self.jid.split('@')[0]
			userNameToSend = to.split('@')[0]
			message_to_send = {'from': self.algorithm_data[userName], 'to': self.algorithm_data[userNameToSend], 'route': [self.algorithm_data[userName]], 'distance': 0, 'message': message, "algorithm": self.algorithm}

			selfNode = self.algorithm_data[self.jid.split('@')[0]]
			neighbours = self.algorithm_data['config'][selfNode]
			neighbours_jid = [jid for jid in list(self.algorithm_data.keys()) if jid != 'config' and self.algorithm_data[jid] in neighbours]

			if message_to_send['to'] != self.algorithm_data[self.jid.split('@')[0]]:
				for jid in neighbours_jid:
					if  message_to_send['from'] != jid:
						message_to_send['distance'] += 1
						self.send_message(
							mto=f'{jid}@alumchat.fun',
							mbody=json.dumps(message_to_send),
							mtype='chat'
						)
						print('message sent to', jid)
						time.sleep(1)
		elif self.algorithm == 'link_state':
			nodes = "".join(self.algorithm_data['config'].keys())
			graph = Graph(len(nodes))
			print('NODES:', nodes)


	def flooding(self, algorithm_data, message):
		selfNode = algorithm_data[self.jid.split('@')[0]]
		neighbours = algorithm_data['config'][selfNode]
		neighbours_jid = [jid for jid in list(algorithm_data.keys()) if jid != 'config' and algorithm_data[jid] in neighbours]
		message = json.loads(message['body'])

		print('Se tiene que enviar a los siguientes nodos:', neighbours)
		print('Se tiene que enviar a los siguientes jids:', neighbours_jid)

		# check to which nodes the message has been send
		already_send_nodes = []
		for node in message['route']:
			reciviers_from_node = algorithm_data['config'][node]
			for node_reciver in reciviers_from_node:
				if node_reciver in already_send_nodes:
					continue
				else:
					already_send_nodes.append(node_reciver)
		print('Ya se envio a:', already_send_nodes)
		if message['to'] != self.algorithm_data[self.jid.split('@')[0]] and selfNode not in message['route']:
			for jid in neighbours_jid:
				if  message['from'] != algorithm_data[jid] and algorithm_data[jid] not in already_send_nodes:
					message['route'].append(algorithm_data[self.jid.split('@')[0]])
					message['distance'] += 1
					self.send_message(
						mto=f'{jid}@alumchat.fun',
						mbody=json.dumps(message),
						mtype='chat'
					)
					print('message sent to', jid)
					time.sleep(1)
		else:
			print(f"""
				Tienes un nuevo mensaje de: {message['from']}\n
				El cual paso por los nodos: {message['route']}\n
				El mensaje dice:\n
				{message['message']}
			""")
