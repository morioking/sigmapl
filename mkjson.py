#!/usr/bin/python
# coding: UTF-8
import sys
from datetime import datetime as dt
import json
import re
import copy
import random

class DataClass:
	def __init__(self):
		self.__file = ""
		self.__data = ""

	def load_json(self, file):
		f = open(file, "r")
		self.__data = json.load(f)
		f.close()
	
	def show(self):
		print json.dumps(self.__data, indent = 4)
	
	def set_data(self, data):
		self.__data = data

	def get_data(self):
		return self.__data
	
	def get_nodes(self):
		return self.__data["nodes"]

	def get_nodes_count(self):
		return len(self.__data["nodes"])
		
	def get_node_id(self, i):
		return self.__data["nodes"][i]["id"]

	def get_node_size(self, i):
		return self.__data["nodes"][i]["size"]
	
	def get_node_size_with_id(self, id):
		return self.get_node_size(self.get_node_index_with_id(id))
		
	def get_node_label(self, i):
		return self.__data["nodes"][i]["label"]
	
	def get_node_id_with_label(self, label):
		id = "none"
		for i in range(len(self.__data["nodes"])):
			if label.find(self.__data["nodes"][i]["label"]) == 0:
				# hit
				id = self.__data["nodes"][i]["id"]

		return id
	
	def get_node_index_with_id(self, id):
		index = -1
		for i in range(len(self.__data["nodes"])):
			if self.__data["nodes"][i]["id"] == id:
				index = i
		return index
	
	def set_node_x(self, id, x):
		pass

	def set_node_y(self, id, y):
		pass

	def set_node_color(self, id, color):
		pass

	def set_node_label(self, id, label):
		pass
	
	def set_node_size(self, i, size):
		self.__data["nodes"][i]["size"] = size

	def set_node_size_with_id(self, id, size):
		self.set_node_size(self.get_node_index_with_id(id), size)

	def set_node_id(self, i, id):
		self.__data["nodes"][i]["id"] = id

	def create_new_node(self, color, label, y, x, id, size):
		self.__data["nodes"].append({"color":color, "label":label, "y":y, "x":x, "id":id, "size":size})
		
	def create_new_edge(self, color, source, id, target):
		self.__data["edges"].append({"color":color, "source":source, "id":id, "target":target})

	def get_edge_id_with_source_target(self, source, target):
		id = "none"
		for i in range(len(self.__data["edges"])):
			if self.__data["edges"][i]["source"] == source:
				if self.__data["edges"][i]["target"] == target:
					# hit
					id = self.__data["edges"][i]["id"]
		return id
		
	def get_edge_index_with_id(self, id):
		index = -1
		for i in range(len(self.__data["edges"])):
			if self.__data["edges"][i]["id"] == id:
				index = i
		return index

	def get_edges_count(self):
		return len(self.__data["edges"])

	def get_edge_source(self, i):
		return self.__data["edges"][i]["source"]

	def get_edge_source_with_id(self, id):
		return self.get_edge_source(self.get_edge_index_with_id(id))
	
	def get_edge_target(self, i):
		return self.__data["edges"][i]["target"]

	def get_edge_target_with_id(self, id):
		return self.get_edge_target(self.get_edge_index_with_id(id))
		
	def get_edge_id(self, i):
		return self.__data["edges"][i]["id"]

	def set_edge_id(self, i, id):
		self.__data["edges"][i]["id"] = id
	
	def set_edge_source(self, i, source):
		self.__data["edges"][i]["source"] = source
	
	def set_edge_source_with_id(self, id, source):
		self.set_edge_source(self.get_edge_index_with_id(id), source)

	def set_edge_target(self, i, target):
		self.__data["edges"][i]["target"] = target
	
	def set_edge_target_with_id(self, id, target):
		self.set_edge_target(self.get_edge_index_with_id(id), target)
		
	def del_edge(self, i):
		self.__data["edges"].pop(i)

	def del_edge_with_id(self, id):
		self.del_edge(self.get_edge_index_with_id(id))

		
class M3u8Class(DataClass):
	def __init__(self):
		DataClass.__init__(self)
		DataClass.set_data(self, {"nodes":[], "edges":[]})
		self.__new_node_ids = []
		self.__old_node_ids = []
		self.__new_edge_ids = []
		self.__old_edge_ids = []
		self.__labels = []
		
	def load_m3u8(self, file):
		print "loading",file, "..."
		f = open(file, "r")
		labels = []
		#self.__data = {"nodes":[], "edges":[]}
		for line in f:
			if re.match("#EXTINF",line):
				label = re.sub("#EXTINF(.[0-9]{3,4}[,])","",line).strip()
				self.__labels.append(label)
				print "    import ", label
		f.close()

		print "finish loading!"
		
	def get_m3u8_label(self, i):
		return self.__labels[i]
		
	def get_m3u8_labels_count(self):
		return len(self.__labels)
		
def mixplaylist(pl1, pl2):
	list_pl1 = []
	list_pl2 = []
	list_outpl = []
	f = open(pl1,"r")
	i = 0
	for line in f:
		# first line EXT1M3U skipped
		if i != 0:
			list_pl1.append(line)
		elif i == 0:
			header = line
		i += 1
	f.close()

	f = open(pl2,"r")
	i = 0
	for line in f:
		# first line EXTM3U skipped
		if i != 0:
			list_pl2.append(line)
		i += 1
	f.close()

	# import pdb; pdb.set_trace()
	idx_a = 0
	idx_b = 0
	while idx_a < len(list_pl1):
		if idx_a != len(list_pl1):
			list_outpl.append(list_pl1[idx_a])
			idx_a += 1
		if idx_a != len(list_pl1):
			list_outpl.append(list_pl1[idx_a])
			idx_a += 1
		if idx_b != len(list_pl2):
			list_outpl.append(list_pl2[idx_b])
			idx_b += 1
		if idx_b != len(list_pl2):
			list_outpl.append(list_pl2[idx_b])
			idx_b += 1

	list_outpl.insert(0, header)

	tdatetime = dt.now()
	tstr = tdatetime.strftime('%Y-%m-%d')
	file3 = "MIXED HISTORY_"+tstr+".m3u8"
	f = open(file3, "w")
	for line in list_outpl:
		f.write(line)
	f.close()

	print ""
	print "finish mixing!!"
	print "the mixed playlist file is",file3
	print ""

if __name__ == "__main__":

	# load json data
	data = DataClass()
	data.load_json("data.json")
	m3u8 = ""

	while 1:
		print "type command..."
		input_line = raw_input()
		if input_line == "exit":
			break
		elif input_line == "mixpl":
			print ""
			print "mix 2 playlist mutually..."
			print "input fist playlist"
			pl1 = raw_input()
			print "input second playlist"
			pl2 = raw_input()
			mixplaylist(pl1, pl2)
		elif input_line == "load":
			# sequence diagram
			# https://creately.com/diagram/isi7szk61/ZdBFzRm5MscjkiipVY4ee11xM%3D
			print "load m3u8 format playlist."
			print "select m3u8 file..."
			input_file = raw_input()
			#input_file = "test.m3u8"
			m3u8 = M3u8Class()
			m3u8.load_m3u8(input_file)
			for i in range(m3u8.get_m3u8_labels_count()):
				print m3u8.get_m3u8_label(i)
				m3u8.create_new_node("rgb(255,204,102)", m3u8.get_m3u8_label(i), 0, 0, "", 1)

			# update node id for m3u8 data
			new_node_id_number = data.get_nodes_count()
			for i in range(m3u8.get_nodes_count()):
				id = data.get_node_id_with_label(m3u8.get_node_label(i))
				if id == "none":
					m3u8.set_node_id(i, "n"+str(new_node_id_number))
					new_node_id_number += 1
				else:
					m3u8.set_node_id(i, id)
			#m3u8.show()
			# create edge for m3u8 data
			for i in range(m3u8.get_nodes_count()-1):
				source = m3u8.get_node_id(i)
				target = m3u8.get_node_id(i + 1)
				m3u8.create_new_edge("rgb(128, 128, 128)", source, "", target)
			#m3u8.show()
			# update edge id for m3u8
			for i in range(m3u8.get_edges_count()):
				m3u8.set_edge_id(i, data.get_edge_id_with_source_target(m3u8.get_edge_source(i), m3u8.get_edge_target(i)))
			m3u8.show()
		elif input_line == "set":
			print "set m3u8 to data"
			# process nodes
			new_node_id_number = data.get_nodes_count()
			for i in range(m3u8.get_nodes_count()):
				m = re.search("\d+", m3u8.get_node_id(i))
				#if m3u8.get_node_id(i) == "none":
				if m.group() >= new_node_id_number:
					posx = random.uniform(-1,1)
					posy = random.uniform(-1,1)
					size = 1
					color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"
					data.create_new_node(color, m3u8.get_node_label(i), posy, posx, m3u8.get_node_id(i), size)
				else:
					data.set_node_size_with_id(m3u8.get_node_id(i), data.get_node_size_with_id(m3u8.get_node_id(i)) + 1)
			# process edges
			new_edge_id_number = data.get_edges_count()
			for i in range(m3u8.get_edges_count()): 
				if m3u8.get_edge_id(i) == "none":
					color = "rgb(128, 128, 128)"
					id = "e"+str(new_edge_id_number)
					data.create_new_edge(color, m3u8.get_edge_source(i), id, m3u8.get_edge_target(i))
					new_edge_id_number += 1
			data.show()
		elif input_line == "commit":
			f = open ("data.json", "w")
			json.dump(data.get_data(), f)
			f.close()
			print "commit data.json"
			break
		elif input_line == "del":
			print "type edges index"
			id = raw_input()
			data.del_edge_with_id(id)
			data.show()
		elif input_line == "show":
			data.show()
		else:
			print "again"






