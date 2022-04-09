

# http://timgolden.me.uk/python/wmi/tutorial.html
# https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-tasks--performance-monitoring
# https://stackoverflow.com/questions/37710244/retrieve-formatted-performance-data-from-wmi

import wmi
import time


class pyperfmon():

	connections = {}

	# def __init__(self):
	# 	self.connect()

	def connect(self, machinename=".", username=None, password=None):
		alias = "localhost"
		if machinename != ".":
			alias = machinename.lower()
		if alias not in self.connections:
			self.connections[alias] = {}
		if "connection" not in self.connections[alias]:
			self.connections[alias]["connection"] = wmi.WMI(machinename)

		self._loadPerfObjects(alias)


	def _loadPerfObjects(self, alias="localhost"):
		c = self.connections[alias]["connection"]
		if "objects" not in self.connections[alias]:
			self.connections[alias]["objects"] = {}

		perf_objs = c.subclasses_of("Win32_PerfFormattedData")
		# print(perf_classes)
		for obj in perf_objs:
			# if obj == "Win32_PerfFormattedData_PerfOS_System":
				cstr = "c.{}".format(obj)
				cobj = eval(cstr)
				# print(cobj)
				sobj = str(cobj)
				# print(sobj)

				# s = sobj.find(": Win32_PerfFormattedData{") + len(": Win32_PerfFormattedData{")
				s = sobj.find("{") + len("{")
				sobject = sobj[0:s-1]
				# print("sobject:", sobject, "\n")

				ons = sobject.find("DisplayName(\"") + len("DisplayName(\"")
				one = sobject.find("\")", ons+1)
				ObjectName = sobject[ons:one]
				# print("ObjectName:", ObjectName)

				if ObjectName not in self.connections[alias]["objects"]:
					self.connections[alias]["objects"][ObjectName] = {}
					self.connections[alias]["objects"][ObjectName]["Name"] = ObjectName
					self.connections[alias]["objects"][ObjectName]["ObjectName"] = obj
					self.connections[alias]["objects"][ObjectName]["counters"] = {}

				# s = sobj.find(obj) + len(obj)
				# s = sobj.find("Win32_PerfFormattedData{") + len("Win32_PerfFormattedData{")
				e = sobj.find("}")
				scounters = sobj[s+1:e]
				lscounters = scounters.split(";")
				# print("lscounters:", lscounters)

				# if ObjectName == "Processor":
				# 	exit()

				for counter in lscounters:

					# print("counter:", counter)

					cs = counter.find("DisplayName(\"") + len("DisplayName(\"")
					ce = counter.find("\")", cs+1)
					counterName = counter[cs:ce]
					# print("counterName:", counterName)

					if len(counterName)>0:

						cos = counter.find("Counter(\"") + len("Counter(\"")
						coe = counter.find("\")", cos+1)
						CounterObjectName = counter[cos:coe]
						# print("CounterObjectName:", CounterObjectName)

						if counterName not in self.connections[alias]["objects"][ObjectName]["counters"]:
							self.connections[alias]["objects"][ObjectName]["counters"][counterName] = {}
							self.connections[alias]["objects"][ObjectName]["counters"][counterName]["Name"] = counterName
							self.connections[alias]["objects"][ObjectName]["counters"][counterName]["ObjectName"] = CounterObjectName


	def getCounter(self, counterpath="None", machinename="localhost"):
		alias = machinename.lower()
		if alias not in self.connections:
			self.connect(machinename)

		tplresult = (counterpath, "ERR: Not Found.")
		counterarr = counterpath.split('\\')

		object = counterarr[0]
		counter = counterarr[-1]
		if len(counterarr)>2:
			instance = counterarr[1]
		else:
			instance = "0"

		# print("object:", object, "	counter:", counter)
		# print(self.connections[alias]["objects"][object])
		if object in self.connections[alias]["objects"]:
			if counter in self.connections[alias]["objects"][object]["counters"]:
				try:
					c = self.connections[alias]["connection"]

					if "cobjs" not in self.connections[alias]["objects"][object]:
						costr = "c.{}".format(self.connections[alias]["objects"][object]["ObjectName"])

						# print("eval(costr):", eval(costr))
						# print("eval(costr)():", eval(costr)())
						cobjs = eval(costr)()
						self.connections[alias]["objects"][object]["cobjs"] = {}

						scobjs = str(cobjs)
						lscobjs = scobjs.split(",")

						if len(cobjs)>1:
							i = 0
							for cobj in cobjs:
								scobj = str(cobj)
								scobj = lscobjs[i]
								# print(scobj)
								i += 1

								ins = scobj.find("Name=\"") + len("Name=\"")
								ine = scobj.find("\"'", ins+1)
								instancei = scobj[ins:ine]
								# print("instancei:", instancei)

								self.connections[alias]["objects"][object]["cobjs"][instancei] = cobj

						else:
							instancei = "0"
							cobj = eval(costr)()[0]
							self.connections[alias]["objects"][object]["cobjs"][instancei] = cobj

					cobj = self.connections[alias]["objects"][object]["cobjs"][instance]
					# print("costr:", costr, "	cobj:", cobj)
					ccstr = "cobj.{}".format(self.connections[alias]["objects"][object]["counters"][counter]["ObjectName"])
					value = eval(ccstr)
					tplresult = (counterpath, value)
				except Exception as e:
					tplresult = (counterpath, e)
		return tplresult

	def getCounterObjects(self, machinename="localhost"):
		alias = machinename.lower()
		if alias not in self.connections:
			self.connect(machinename)

		return list(self.connections[alias]["objects"].keys())


	def getCounters(self, ObjectName=None, machinename="localhost"):
		alias = machinename.lower()
		if alias not in self.connections:
			self.connect(machinename)

		if ObjectName in self.connections[alias]["objects"]:

			return list(self.connections[alias]["objects"][ObjectName]["counters"].keys())
