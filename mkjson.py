#!/usr/bin/python
# coding: UTF-8
import sys
from datetime import datetime as dt
import json
import re
import copy
import random

jsondata = []
labels = []
jsonout = []
nodeclasses = []
edgeclasses = []

class NodeClass:
	def __init__(self, label):
		self._color = "rgb(0,255,0)"
		self._label = label
		self._y = 0
		self._x = 0
		self._id = ""
		self._size = 1
		self._isNew = False

	def setLabel(self, label):
		self._label = label
		
	def getLabel(self):
		return self._label

	def setX(self, x):
		self._x = x
	
	def getX(self):
		return self._x
		
	def setY(self, y):
		self._y = y

	def getY(self):
		return self._y
		
	def setColor(self, color):
		self._color = color

	def getColor(self):
		return self._color

	def setId(self, id):
		self._id = id
	
	def getId(self):
		return self._id

	def setSize(self, size):
		self._size = size
	
	def getSize(self):
		return self._size
		
	def setIsNew(self, isNew):
		self._isNew = isNew

	def getIsNew(self):
		return self._isNew

class EdgeClass:
	def __init__(self):
		self._color = "rgb(128,128,128)"
		self._source = ""
		self._id = ""
		self._target = ""
		self._isNew = False
		
	def setColor(self,color):
		self._color = color

	def getColor(self):
		return self._color
		
	def setSource(self, source):
		self._source = source
		
	def getSource(self):
		return self._source
		
	def setId(self, id):
		self._id = id
	
	def getId(self):
		return self._id
		
	def setTarget(self, target):
		self._target = target
	
	def getTarget(self):
		return self._target
		
	def setIsNew(self, isNew):
		self._isNew = isNew
	
	def getIsNew(self):
		return self._isNew
		
if __name__ == "__main__":

	print ""
	print "start mixing..."
	print ""

	# param = sys.argv
	# file1 = param[1]
	# print "import labels file is",file1

	# load json data
	f = open("data.json", "r")
	jsondata = json.load(f)
	f.close()

	jsonout = copy.deepcopy(jsondata)

	# load m3u8
	f = open("test.m3u8", "r")
	for line in f:
		if re.match("#EXTINF",line):
			labels.append(re.sub("#EXTINF(.*[,])","",line))
	f.close()

	# making NodeClass and nodeclasses
	new_node_id = len(jsondata["nodes"]) - 1
	nodeclasses_idx = 0
	for label in labels:
		isHit = False
		idxHit = 0
		node_size = 1
		nodeclasses.append(NodeClass(label.strip()))
		print "searching ", label.strip(), "from data.json...."
		for i in range(len(jsondata["nodes"])):
			# print "  compairing ", label.strip(), "VS", jsondata["nodes"][i]["label"], label.find(jsondata["nodes"][i]["label"])
			if label.find(jsondata["nodes"][i]["label"]) == 0:
				# hit
				isHit = True
				idxHit = i
				break
			elif label.find(jsondata["nodes"][i]["label"]) == -1:
				# not-hit
				isHit = False
			else:
				print "unknown hit"

		nodeclasses[nodeclasses_idx].setIsNew = not(isHit)
		if isHit:
			id = jsondata["nodes"][idxHit]["id"]
		else:
			id = "n"+str(new_node_id)
		nodeclasses[nodeclasses_idx].setId(id)
		
		nodeclasses_idx += 1
		
	# making EdgeClass and edgeclasses
	for i in range(len(nodeclasses)-1):
		source = nodeclasses[i].getId()
		target = nodeclasses[i+1].getId()
		
		print "source", source, " target", target
	
	
		# if isHit == True:
		# 	print "    search result.... isHit = ", isHit, "make the size of the node bigger"
		# 	node_size = jsondata["nodes"][idxHit]["size"]
		# 	node_id = jsondata["nodes"][idxHit]["id"]
		# 	posx = int(random.random()*10)
		# 	posy = int(random.random()*10)
		# 	# print "      -> the size of index is", node_size
		# 	# print "      -> the id of index is", node_id
		# 	jsonout["nodes"][idxHit]["size"] = node_size + 1
		# 	jsonout["nodes"][idxHit]["x"] = posx
		# 	jsonout["nodes"][idxHit]["y"] = posy

		# if isHit == False:
		# 	print "    search result.... isHit = ", isHit, "make new node..."
		# 	new_node_id += 1
		# 	color = "rgb(0,0,255)"
		# 	label = label.strip()
		# 	identfy = "n"+str(new_node_id)
		# 	posx = int(random.random()*10)
		# 	posy = int(random.random()*10)
		# 	node_size = 1
		# 	jsonout["nodes"].append({"color":color, "label":label, "x":posx, "y":posy, "id":identfy, "size":node_size})

	# making edges


	
	# search edges


	print "------------------jsondata------------------"
	print json.dumps(jsondata, indent = 4)
	print "------------------jsonout------------------"
	print json.dumps(jsonout, indent = 4)

	# f = open ("data.json", "w")
	# json.dump(jsonout, f)
	# f.close()



	for nc in nodeclasses:
		print nc.getLabel(), nc.getIsNew(), nc.getX(), nc.getY(), nc.getColor(), nc.getId()

	ec = EdgeClass()
	print ec.getColor(), ec.getSource(), ec.getId(), ec.getTarget(), ec.getIsNew()

	# comment no sample
	# print json.dumps(jsondata["nodes"], sort_keys = True, indent = 4)
	# print len(jsondata["nodes"])
	# print json.dumps(jsondata, sort_keys = True, indent = 4)
	# print json.dumps(jsondata["nodes"][0]["color"], indent = 4)
	# print jsondata["nodes"][1]


	# for i in range(len(jsondata["nodes"])):
	# 	hit_index = 0
	# 	for label in labels:
	# 		print "compair ", label.strip(), "with", jsondata["nodes"][i]["label"], label.find(jsondata["nodes"][i]["label"])
	# 		if label.find(jsondata["nodes"][i]["label"]) != -1:
	# 			hit_index = i
	# 	if hit_index == 0:
	# 		#not hit
	# 		print "not hit"
	# 	else:
	# 		#hit
	# 		print "hit"

	# f = open(file1,"r")
	# i = 0
	# for line in f:
	# 	# first line EXTM3U skipped
	# 	if i != 0:
	# 		list_a.append(line)
	# 	elif i == 0:
	# 		header = line
	# 	i += 1
	# f.close()

	# f = open(file2,"r")
	# i = 0
	# for line in f:
	# 	# first line EXTM3U skipped
	# 	if i != 0:
	# 		list_b.append(line)
	# 	i += 1
	# f.close()

	# # import pdb; pdb.set_trace()
	# idx_a = 0
	# idx_b = 0
	# while idx_a < len(list_a):
	# 	if idx_a != len(list_a):
	# 		list_c.append(list_a[idx_a])
	# 		idx_a += 1
	# 	if idx_a != len(list_a):
	# 		list_c.append(list_a[idx_a])
	# 		idx_a += 1
	# 	if idx_b != len(list_b):
	# 		list_c.append(list_b[idx_b])
	# 		idx_b += 1
	# 	if idx_b != len(list_b):
	# 		list_c.append(list_b[idx_b])
	# 		idx_b += 1

	# list_c.insert(0, header)

	# tdatetime = dt.now()
	# tstr = tdatetime.strftime('%Y-%m-%d')
	# file3 = "MIXED HISTORY_"+tstr+".m3u8"
	# f = open(file3, "w")
	# for line in list_c:
	# 	f.write(line)
	# f.close()

	print ""
	print "finish mixing!!"
	# print "the mixed labels file is",file3
	# print ""
