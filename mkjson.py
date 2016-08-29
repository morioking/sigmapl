#!/usr/bin/python
# coding: UTF-8
import sys
from datetime import datetime as dt
import json
import re
import copy
import random

jsondata = []
jsonout = []
nodeclasses = []
edgeclasses = []

class JsonClass:
	def __init__(self, file):
		self.__file = file
		f = open(file, "r")
		self.__jsondata = json.load(f)
		f.close()

	def show(self):
		print json.dumps(self.__jsondata, indent = 4)
		
	def get_json(self):
		return self.__jsondata
	
	def get_nodes(self):
		return self.__jsondata["nodes"]

	def get_node_id(self, idx):
		return self.__jsondata["nodes"][idx]["id"]

	def get_node_size(self, idx):
		return self.__jsondata["nodes"][idx]["size"]

	def get_node_label(self, idx):
		return self.__jsondata["nodes"][idx]["label"]
		
class M3u8Class:
	def __init__(self, file):
		self.__file = file
		self.__labels = []
		f = open(file, "r")
		for line in f:
			print "import ",file, line.strip()
			if re.match("#EXTINF",line):
				self.__labels.append(re.sub("#EXTINF(.*[,])","",line).strip())
		f.close()
	
	def get_label(self, i):
		return self.__labels[i]
		
	def get_labels(self):
		return self.__labels

	def show_labels(self):
		for label in self.__labels:
			print label

class NodesClass:
	def __init__(self):
		self.__nodeclasses = []

	def append_node(self, nodeclass):
		self.__nodeclasses.append(nodeclass)
		
	def get_nodes_count(self):
		return len(self.__nodeclasses)
	
	def get_node(self, num):
		return self.__nodeclasses[num]


class NodeClass:
	def __init__(self, label):
		self._color = "rgb(0,255,0)"
		self._label = label
		self._y = 0
		self._x = 0
		self._id = ""
		self._size = 1
		self._isNew = False

	def set_label(self, label):
		self._label = label
		
	def get_label(self):
		return self._label

	def set_x(self, x):
		self._x = x
	
	def get_x(self):
		return self._x
		
	def set_y(self, y):
		self._y = y

	def get_y(self):
		return self._y
		
	def set_color(self, color):
		self._color = color

	def get_color(self):
		return self._color

	def set_id(self, id):
		self._id = id
	
	def get_id(self):
		return self._id

	def set_size(self, size):
		self._size = size
	
	def get_size(self):
		return self._size
		
	def set_is_new(self, isNew):
		self._isNew = isNew

	def get_is_new(self):
		return self._isNew

class EdgeClass:
	def __init__(self):
		self._color = "rgb(128,128,128)"
		self._source = ""
		self._id = ""
		self._target = ""
		self._isNew = False
		
	def set_color(self,color):
		self._color = color

	def get_color(self):
		return self._color
		
	def set_source(self, source):
		self._source = source
		
	def get_source(self):
		return self._source
		
	def set_id(self, id):
		self._id = id
	
	def get_id(self):
		return self._id
		
	def set_target(self, target):
		self._target = target
	
	def get_target(self):
		return self._target
		
	def set_is_new(self, isNew):
		self._isNew = isNew
	
	def get_is_new(self):
		return self._isNew


def import_playlist(m3u8, json_class):
	jsonout = copy.deepcopy(jsondata)
	m3u8_class = M3u8Class(m3u8)
	labels = m3u8_class.get_labels()
	input_json_class = json_class

	# making NodeClass and nodeclasses
	new_node_id = len(input_json_class.get_nodes()) - 1
	nodeclasses_idx = 0
	for label in labels:
		isHit = False
		idxHit = 0
		node_size = 1
		nodeclasses.append(NodeClass(label))
		for i in range(len(input_json_class.get_nodes())):
			if label.find(input_json_class.get_node_label(i)) == 0:
				# hit
				isHit = True
				idxHit = i
				break
			elif label.find(input_json_class.get_node_label(i)) == -1:
				# not-hit
				isHit = False
			else:
				print "unknown hit"

		nodeclasses[nodeclasses_idx].set_is_new(not(isHit))
		if isHit:
			id = input_json_class.get_node_id(idxHit)
			posx = random.uniform(-1,1)
			posy = random.uniform(-1,1)
			size = input_json_class.get_node_size(idxHit) + 1
			color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"
		else:
			new_node_id += 1
			id = "n"+str(new_node_id)
			posx = random.uniform(-1,1)
			posy = random.uniform(-1,1)
			size = 1
			color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"

		nodeclasses[nodeclasses_idx].set_id(id)
		nodeclasses[nodeclasses_idx].set_x(posx)
		nodeclasses[nodeclasses_idx].set_y(posy)
		nodeclasses[nodeclasses_idx].set_size(size)
		nodeclasses[nodeclasses_idx].set_color(color)
		nodeclasses_idx += 1

	# making EdgeClass and edgeclasses
	# for i in range(len(nodeclasses)-1):
		# source = nodeclasses[i].get_id()
		# target = nodeclasses[i+1].get_id()
		# ec = EdgeClass()
		# ec.set_source(source)
		# ec.set_target(target)
		# edgeclasses.append(ec)

	# # search isNew for EdgeClass
	# new_edge_id = len(input_json_class.get_json()["edges"]) - 1
	# for ec in edgeclasses:
		# isHit = False
		# source = ec.get_source()
		# target = ec.get_target()
		# for i in range(len(input_json_class.get_json()["edges"])):
			# if (input_json_class.get_json()["edges"][i]["source"] == source) and (input_json_class.get_json()["edges"][i]["target"] == target):
				# isHit = True
				# break
			# else:
				# isHit = False

		# #print "edge",isHit
		# ec.set_is_new(not(isHit))
		# if isHit:
			# id = input_json_class.get_json()["edges"][i]["id"]
		# else:
			# new_edge_id += 1
			# id = "e"+str(new_edge_id)

		# ec.set_id(id)

	# # update jsonout for node
	# for nc in nodeclasses:
		# if nc.get_is_new():
			# jsonout["nodes"].append({"color":nc.get_color(), "label":nc.get_label(), "y":nc.get_y(), "x":nc.get_x(), "id":nc.get_id(), "size":nc.get_size()})
		# else:
			# for i in range(len(input_json_class.get_nodes())):
				# if input_json_class.get_nodes()[i]["id"] == nc.get_id():
					# jsonout["nodes"][i]["color"] = nc.get_color()
					# jsonout["nodes"][i]["x"] = nc.get_x()
					# jsonout["nodes"][i]["y"] = nc.get_y()
					# jsonout["nodes"][i]["size"] = nc.get_size()


	# # update jsonout for edge
	# for ec in edgeclasses:
		# if ec.get_is_new():
			# jsonout["edges"].append({"color":ec.get_color(), "source":ec.get_source(), "id":ec.get_id(), "target":ec.get_target()})

	# print "------------------jsondata------------------"
	# print json.dumps(jsondata, indent = 4)
	# print "------------------jsonout------------------"
	# print json.dumps(jsonout, indent = 4)
	
	# for nc in nodeclasses:
	# 	print nc.get_label(), nc.get_is_new(), nc.get_x(), nc.get_y(), nc.get_color(), nc.get_id()

	# for ec in edgeclasses:
	# 	print ec.get_color(), ec.get_source(), ec.get_id(), ec.get_target(), ec.get_is_new()

	# f = open ("data.json", "w")
	# json.dump(jsonout, f)
	# f.close()
		
if __name__ == "__main__":

	# load json data
	input_json_class = JsonClass("data.json")
	
	while 1:
		print "enter..."
		input_line = raw_input()
		if input_line == "exit":
			break
		elif input_line == "show":
			print "------------------data.json------------------"
			print input_json_class.show()
			print input_json_class.get_nodes()
			print input_json_class.get_node_label(2)
			print input_json_class.get_node_size(2)
			print input_json_class.get_node_id(2)
		elif input_line == "import":
			import_playlist("test.m3u8", input_json_class)
		elif input_line == "mixpl":
			print ""
			print "mix 2 playlist mutually.....but this function is not implemented yet"
			print "select fist playlist"
			#pl1 = raw_input()
			print "select second playlist"
			#pl2 = raw_input()
		elif input_line == "test":
			print "test NodesClass"
			nc = NodeClass("hoge")
			nsc = NodesClass()
			nsc.append_node(nc)
			print nsc.get_nodes_count()
			print nsc.get_node(0).get_label()
		elif input_line == "test2":
			cl = M3u8Class("test.m3u8")
			cl.show_labels()
		else:
			print "again"






