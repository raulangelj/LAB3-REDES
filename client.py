import slixmpp
import time
import json
from LINK_STATE.dijkstra import Graph
from aioconsole import ainput, aprint
from slixmpp.exceptions import IqError, IqTimeout
from LINK_STATE.dijkstra import dijkstra_algorithm, Graph, print_result
from DISTANCE_VECTOR.bellman import Graph_Bellman

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
		# user = str(message['from']).split('@')[0]
		# await aprint(f'{user}: {message["body"]}')
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
		elif self.algorithm == 'distance_vector':
			try:
				if not self.algorithm_data:
					# READ JSON FILE FOR DISTANCE_VECTOR
					f = open('./DISTANCE_VECTOR/DISTANCE_VECTOR.json')
					algorithm_data = json.load(f)
					self.algorithm_data = algorithm_data
					print(algorithm_data)
				self.distance_vector(self.algorithm_data, message)
			except Exception as e:
				print(e)
		elif self.algorithm == 'link_state':
			try:
				if not self.algorithm_data:
					# READ JSON FILE FOR FLOODING
					f = open('./LINK_STATE/LINK_STATE.json')
					algorithm_data = json.load(f)
					self.algorithm_data = algorithm_data
					print(algorithm_data)
				self.link_state(self.algorithm_data, message)
			except Exception as e:
				print(e)

	async def send_new_message(self, message, to):
		if self.algorithm == 'flooding':
			userName = self.jid.split('@')[0]
			userNameToSend = to.split('@')[0]
			message_to_send = {'from': self.algorithm_data[userName], 'to': self.algorithm_data[userNameToSend], 'node_jumps': 1, 'route': [self.algorithm_data[userName]], 'distance': 0, 'message': message, "algorithm": self.algorithm}

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
		elif self.algorithm == 'distance_vector':
			try:
				algorithm_data = self.algorithm_data
				sender_userName = self.jid.split('@')[0]
				recivier_userName = to.split('@')[0]
				sender_node = algorithm_data[sender_userName]
				recivier_node = algorithm_data[recivier_userName]
				# print(algorithm_data)
				nodes = list(algorithm_data['config'].keys())
				config = algorithm_data['config']
				print('NODES:', nodes, len(nodes))
				# Creamos nuestro grafo
				nodes_complete = "".join(nodes)
				g = Graph_Bellman(len(nodes))
				print('G:', g)
				for node in config:
					for neighbour in config[node]:
						print('NODE:', node, 'NEIGHBOUR:', neighbour)
						for key in neighbour:
							g.addEdge(nodes_complete.find(node), nodes_complete.find(key) , neighbour[key])
				
				sender_index = nodes_complete.find(sender_node)
				recivier_index = nodes_complete.find(recivier_node)
				route, weight = g.BellmanFord(sender_index, recivier_index)
				print('ROUTE:', route)
				print('WEIGHT:', weight)

				# convertir route a los nodos de la red
				route_nodes = [nodes[node] for node in route]
				# prepare message to send
				message_to_send = {
					'from': self.boundjid.bare,
					'to': to,
					'message': message,
					'algorithm': self.algorithm,
					'route': route_nodes,
					'distance': weight,
					'node_jumps': 1
				}
				
				# find the key from algorithm_data that values matches th route_nodes[1]
				for key in algorithm_data.keys():
					if algorithm_data[key] == route_nodes[1]:
						real_jid = key
						break
				self.send_message(
					mto=f'{real_jid}@alumchat.fun',
					mbody=json.dumps(message_to_send),
					mtype='chat'
				)
				print('message_to_send:', message_to_send)
				print('message sent to', f'{real_jid}@alumchat.fun')

			except Exception as e:
				print('Error:', e)

		elif self.algorithm == 'link_state':
			try:
				algorithm_data = self.algorithm_data
				sender_userName = self.jid.split('@')[0]
				recivier_userName = to.split('@')[0]
				sender_node = algorithm_data[sender_userName]
				recivier_node = algorithm_data[recivier_userName]
				# print(algorithm_data)
				nodes = list(algorithm_data['config'].keys())
				print('NODES:', nodes, len(nodes))

				init_grapgh = {node: {} for node in nodes}

				for key in (algorithm_data['config'].keys()):
					for key2 in algorithm_data['config'][key]:
						for _ in range(len(key2)):
							first_node = list(key2.keys())[0]
							init_grapgh[key][first_node] = key2[first_node]
				print('init_grapgh:', init_grapgh)
				graph = Graph(nodes, init_grapgh)
				previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=sender_node)
				route, weight = print_result(previous_nodes, shortest_path, start_node=sender_node, target_node=recivier_node)
				best_route = route[::-1]
				print('best_route:', best_route)
				print('weight:', weight)
				# prepare message to send
				message_to_send = {
					'from': self.boundjid.bare,
					'to': to,
					'message': message,
					'algorithm': self.algorithm,
					'route': best_route,
					'distance': weight,
					'node_jumps': 1
				}
				# find the key from algorithm_data that values matches th best_route[1]
				for key in algorithm_data.keys():
					if algorithm_data[key] == best_route[1]:
						real_jid = key
						break
				self.send_message(
					mto=f'{real_jid}@alumchat.fun',
					mbody=json.dumps(message_to_send),
					mtype='chat'
				)
				print('message_to_send:', message_to_send)
				print('message sent to', f'{real_jid}@alumchat.fun')
			except Exception as e:
				print('Error:', e)



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
		print('Se envio anteriormente a:', already_send_nodes)
		if message['to'] != self.algorithm_data[self.jid.split('@')[0]] and selfNode not in message['route']:
			for jid in neighbours_jid:
				if  message['from'] != algorithm_data[jid] and algorithm_data[jid] not in already_send_nodes:
					message['route'].append(algorithm_data[self.jid.split('@')[0]])
					message['distance'] += 1
					message['node_jumps'] += 1
					self.send_message(
						mto=f'{jid}@alumchat.fun',
						mbody=json.dumps(message),
						mtype='chat'
					)
					print('message from node (', message['from'] ,')')
					print('message sent to', jid, ' node (', message['to'] ,')')
					time.sleep(1)
		else:
			jid_sender = ''
			jid_reciver = ''
			for keys in algorithm_data.keys():
				if algorithm_data[keys] == message['to']:
					jid_reciver = keys
				if algorithm_data[keys] == message['from']:
					jid_sender = keys
			print(f"""
				Tienes un nuevo mensaje de: {message['from']} ({jid_sender}@alumchat.fun)\n
				Para {message['to']} ({jid_reciver}@alumchat.fun)\n
				El cual paso por los nodos: {message['route']}\n
				Y se enviaron {message['node_jumps']} (saltos o cantidad de nodos recorridos) veces\n
				El mensaje dice:\n
				{message['message']}
			""")
	
	def distance_vector(self, algorithm_data, message):
		""" 
			Recibir mensaje
		"""
		
		self_username = self.boundjid.bare.split('@')[0]
		self_node = algorithm_data[self_username]
		real_message = json.loads(message['body'])
		node_to_send_index = real_message['node_jumps'] + 1
		
		nodes = list(algorithm_data['config'].keys())
		config = algorithm_data['config']
		# Creamos nuestro grafo
		nodes_complete = "".join(nodes)

		if self.boundjid.bare == str(real_message['to']).split('/')[0]:
			print(f"""
				Tienes un nuevo mensaje de: {real_message['from']} ({algorithm_data[real_message['from'].split('@')[0]]})\n
				Para {real_message['to']} ({algorithm_data[real_message['to'].split('@')[0]]})\n
				El cual paso por los nodos: {real_message['route']}\n
				Y se enviaron {real_message['node_jumps']} (saltos o cantidad de nodos recorridos) veces\n
				Recorrio una distancia minima de {real_message['distance']}
				El mensaje dice:\n
				{real_message['message']}
			""")
		else:
			node_to_send = real_message['route'][node_to_send_index]
			# modify our node_jumps
			real_message['node_jumps'] += 1
			# find the key that matches the node_to_send in algorithm_data
			for key in algorithm_data.keys():
				if algorithm_data[key] == node_to_send:
					jid_to_send = key
					break
			# send the message to the next node
			self.send_message(
				mto=f'{jid_to_send}@alumchat.fun',
				mbody=json.dumps(real_message),
				mtype='chat'
			)
			print('message from node', str(message['from']).split('/')[0])
			print('message sent to', jid_to_send)

	def link_state(self, algorithm_data, message):
		self_username = self.boundjid.bare.split('@')[0]
		self_node = algorithm_data[self_username]
		real_message = json.loads(message['body'])
		node_to_send_index = real_message['node_jumps'] + 1
		# found the real reciver
		if self.boundjid.bare == str(real_message['to']).split('/')[0]:
			print(f"""
				Tienes un nuevo mensaje de: {real_message['from']} ({algorithm_data[real_message['from'].split('@')[0]]})\n
				Para {real_message['to']} ({algorithm_data[real_message['to'].split('@')[0]]})\n
				El cual paso por los nodos: {real_message['route']}\n
				Y se enviaron {real_message['node_jumps']} (saltos o cantidad de nodos recorridos) veces\n
				Recorrio una distancia minima de {real_message['distance']}
				El mensaje dice:\n
				{real_message['message']}
			""")
		else:
			node_to_send = real_message['route'][node_to_send_index]
			# modify our node_jumps
			real_message['node_jumps'] += 1
			# find the key that matches the node_to_send in algorithm_data
			for key in algorithm_data.keys():
				if algorithm_data[key] == node_to_send:
					jid_to_send = key
					break
			# send the message to the next node
			self.send_message(
				mto=f'{jid_to_send}@alumchat.fun',
				mbody=json.dumps(real_message),
				mtype='chat'
			)
			print('message from node', str(message['from']).split('/')[0])
			print('message sent to', jid_to_send)
			# print('message ', real_message)


