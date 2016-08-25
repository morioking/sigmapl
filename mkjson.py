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
		print "import m3u8....", line.strip()
		if re.match("#EXTINF",line):
			labels.append(re.sub("#EXTINF(.*[,])","",line).strip())
	f.close()

	print "labels", labels

	# making NodeClass and nodeclasses
	new_node_id = len(jsondata["nodes"]) - 1
	nodeclasses_idx = 0
	for label in labels:
		isHit = False
		idxHit = 0
		node_size = 1
		nodeclasses.append(NodeClass(label))
		for i in range(len(jsondata["nodes"])):
			# print "  compairing ", label, "VS", jsondata["nodes"][i]["label"], label.find(jsondata["nodes"][i]["label"])
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

		nodeclasses[nodeclasses_idx].setIsNew(not(isHit))
		if isHit:
			id = jsondata["nodes"][idxHit]["id"]
			posx = random.uniform(-1,1)
			posy = random.uniform(-1,1)
			size = jsondata["nodes"][idxHit]["size"] + 1
			color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"
		else:
			new_node_id += 1
			id = "n"+str(new_node_id)
			posx = random.uniform(-1,1)
			posy = random.uniform(-1,1)
			size = 1
			color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"

		nodeclasses[nodeclasses_idx].setId(id)
		nodeclasses[nodeclasses_idx].setX(posx)
		nodeclasses[nodeclasses_idx].setY(posy)
		nodeclasses[nodeclasses_idx].setSize(size)
		nodeclasses[nodeclasses_idx].setColor(color)
		nodeclasses_idx += 1

	# making EdgeClass and edgeclasses
	for i in range(len(nodeclasses)-1):
		source = nodeclasses[i].getId()
		target = nodeclasses[i+1].getId()
		ec = EdgeClass()
		ec.setSource(source)
		ec.setTarget(target)
		edgeclasses.append(ec)

	# search isNew for EdgeClass
	new_edge_id = len(jsondata["edges"]) - 1
	for ec in edgeclasses:
		isHit = False
		source = ec.getSource()
		target = ec.getTarget()
		for i in range(len(jsondata["edges"])):
			if (jsondata["edges"][i]["source"] == source) and (jsondata["edges"][i]["target"] == target):
				isHit = True
				break
			else:
				isHit = False

		#print "edge",isHit
		ec.setIsNew(not(isHit))
		if isHit:
			id = jsondata["edges"][i]["id"]
		else:
			new_edge_id += 1
			id = "e"+str(new_edge_id)

		ec.setId(id)


	# update jsonout for node
	for nc in nodeclasses:
		if nc.getIsNew():
			jsonout["nodes"].append({"color":nc.getColor(), "label":nc.getLabel(), "y":nc.getY(), "x":nc.getX(), "id":nc.getId(), "size":nc.getSize()})
		else:
			for i in range(len(jsondata["nodes"])):
				if jsondata["nodes"][i]["id"] == nc.getId():
					jsonout["nodes"][i]["color"] = nc.getColor()
					jsonout["nodes"][i]["x"] = nc.getX()
					jsonout["nodes"][i]["y"] = nc.getY()
					jsonout["nodes"][i]["size"] = nc.getSize()


	# update jsonout for edge
	for ec in edgeclasses:
		if ec.getIsNew():
			jsonout["edges"].append({"color":ec.getColor(), "source":ec.getSource(), "id":ec.getId(), "target":ec.getTarget()})


	print "------------------jsondata------------------"
	print json.dumps(jsondata, indent = 4)
	print "------------------jsonout------------------"
	print json.dumps(jsonout, indent = 4)


	# for nc in nodeclasses:
	# 	print nc.getLabel(), nc.getIsNew(), nc.getX(), nc.getY(), nc.getColor(), nc.getId()

	# for ec in edgeclasses:
	# 	print ec.getColor(), ec.getSource(), ec.getId(), ec.getTarget(), ec.getIsNew()

	# f = open ("data.json", "w")
	# json.dump(jsonout, f)
	# f.close()

