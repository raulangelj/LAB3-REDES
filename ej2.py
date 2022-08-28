from copyreg import constructor
import json
import numpy as np
# from LINK_STATE.dijkstra import Graph
from LINK_STATE.dijkstra import dijkstra_algorithm, Graph, print_result

data_file = './LINK_STATE/LINK_STATE.json'
# READ JSON FILE FOR FLOODING
# try:
#   f = open(data_file)
#   algorithm_data = json.load(f)
#   # print(algorithm_data)
#   nodes = "".join(algorithm_data['config'].keys())
#   graph = Graph(len(nodes))
#   # print('NODES:', nodes, len(nodes))
#   adapted_array = []
#   for key in algorithm_data['config']:
#     distances = np.zeros(len(nodes), dtype=int)
#     # print('distances original:', distances)
#     # print('key:', key)
#     for key2 in range(0, len(algorithm_data['config'][key])):
#       first_node = list(algorithm_data['config'][key][key2].keys())[0]
#       # print('EL QUE BUSCO:', first_node)
#       index = nodes.find(first_node)
#       # print('INDEX:', index)
#       # print('KEY2:', key2)
#       # # print('type', type(algorithm_data['config'][key][key2]))
#       # # print('las keys sin:', list(algorithm_data['config'][key][key2].keys()))
#       # print('distance', algorithm_data['config'][key][key2][first_node])
#       distances[index] = algorithm_data['config'][key][key2][first_node]
#       # print('new distances:', distances)
#     # print('distances:', distances)
#     adapted_array.append(list(distances))
#   # print('adapted_array:', adapted_array)
#   graph.graph = adapted_array
#   graph.dijkstra(0)
#   # for i in algorithm_data['config']:
#   #   arr = []
#   #   for j in range(0, len(nodes)):
#   #     # print(nodes[j], 'AAAAA', algorithm_data['config'][i])
#   #     if nodes[j] in algorithm_data['config'][i]:
#   #       arr.append(algorithm_data['config'][i][nodes[j]])
#   #     else:
#   #       arr.append(0)
#   #   adapted_array.append(arr)
#   # # print(adapted_array)
# except Exception as e:
#   print(e)

try:
  f = open(data_file)
  algorithm_data = json.load(f)
  # print(algorithm_data)
  nodes = list(algorithm_data['config'].keys())
  print('NODES:', nodes, len(nodes))

  init_grapgh = {}
  for node in nodes:
    init_grapgh[node] = {}
  print('init_grapgh:', init_grapgh)
  
  for key in (algorithm_data['config'].keys()):
    for key2 in algorithm_data['config'][key]:
      for index in range(0, len(key2)):
        print('key:', key, 'key2:', key2)
        first_node = list(key2.keys())[0]
        init_grapgh[key][first_node] = key2[first_node]
  print('init_grapgh:', init_grapgh)
  graph = Graph(nodes, init_grapgh)
  previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="a")
  print_result(previous_nodes, shortest_path, start_node="a", target_node="d")

except Exception as e:
  print(e)