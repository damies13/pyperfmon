# https://github.com/tjguk/wmi/blob/master/readme.rst
# http://timgolden.me.uk/python/wmi/tutorial.html
# https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-tasks--performance-monitoring
# https://stackoverflow.com/questions/37710244/retrieve-formatted-performance-data-from-wmi

import wmi
import time


class pyperfmon():
    connections = {}
    version="0.2.2"

    def __version__(self)
        return self.version

    def _loadPerfObjects(self, alias="localhost"):
        connection = self.connections[alias]["connection"]
        perfclasses_names = connection.subclasses_of("Win32_PerfRawData")
        for perfclass_name in perfclasses_names:
            perfclass_instance = getattr(connection, perfclass_name)
            perfclass_instance_name = perfclass_instance.qualifiers["DisplayName"]
            if perfclass_instance_name not in self.connections[alias]["objects"]:
                self.connections[alias]["objects"][perfclass_instance_name] = {
                    "Name": perfclass_instance_name,
                    "ObjectName": perfclass_name,
                    "counters": {},
                }

            counters_names = perfclass_instance.properties.keys() # get counter names from list of counters
            for counter_name in counters_names:
                counter = perfclass_instance.wmi_property(counter_name) # get wrapped performance counter object
                # do not include qualifiers such as Name, Caption, Description
                if "DisplayName" not in counter.qualifiers:
                    continue

                counter_display_name = counter.qualifiers["DisplayName"]
                if counter_display_name in self.connections[alias]["objects"][perfclass_instance_name]["counters"]:
                    continue

                self.connections[alias]["objects"][perfclass_instance_name]["counters"][counter_display_name] = {
                    "Name": counter_display_name,
                    "ObjectName": counter_name,
                }

    def connect(self, machinename=".", username=None, password=None):
        alias = "localhost" if machinename == "." else machinename.lower()
        if alias not in self.connections:
            self.connections[alias] = {}

        if "connection" not in self.connections[alias]:
            self.connections[alias]["connection"] =  wmi.WMI(machinename)

        if "objects" not in self.connections[alias]:
            self.connections[alias]["objects"] = {}

        self._loadPerfObjects(alias)

    def getCounter(self, counterpath="None", machinename="localhost"):
        alias = machinename.lower()
        if alias not in self.connections:
            self.connect(machinename)

        counterarr = counterpath.split('\\')
        perfclass_instance_name = counterarr[0]
        counter_display_name = counterarr[-1]
        instance = counterarr[1] if len(counterarr) > 2 else "0"
        perfclass_exists = perfclass_instance_name in self.connections[alias]["objects"]
        counter_display_name_exists = counter_display_name in self.connections[alias]["objects"][perfclass_instance_name]["counters"].keys()
        if not (perfclass_exists and counter_display_name_exists) :
            return (counterpath, "ERR: Not Found.")

        try:
            connection = self.connections[alias]["connection"]
            cstrs = self.connections[alias]["objects"][perfclass_instance_name]["ObjectName"]
            cobjs = getattr(connection, cstrs.replace("Win32_PerfRawData", "Win32_PerfFormattedData"))() # instantiate performance counters object to get fresh data
            self.connections[alias]["objects"][perfclass_instance_name]["cobjs"] = {cobj.Name or "0": cobj for cobj in cobjs} # get individual counters names
            instance_exists =  instance in self.connections[alias]["objects"][perfclass_instance_name]["cobjs"].keys()
            if not instance_exists:
                return (counterpath, "ERR: Not Found.")

            cobj = self.connections[alias]["objects"][perfclass_instance_name]["cobjs"][instance]
            cstr = self.connections[alias]["objects"][perfclass_instance_name]["counters"][counter_display_name]["ObjectName"]

            value = getattr(cobj, cstr)

            return (counterpath, value)
        except Exception as e:
            return (counterpath, e)

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

    def getCounterInstances(self, ObjectName=None, machinename="localhost"):
        alias = machinename.lower()
        if alias not in self.connections:
            self.connect(machinename)

        if ObjectName in self.connections[alias]["objects"]:
            c = self.connections[alias]["connection"]
            cstrs = self.connections[alias]["objects"][ObjectName]["ObjectName"]
            cobjs = getattr(c, cstrs)()
            return [cobj.Name for cobj in cobjs if cobj.Name is not None] # return empty list for single instance counters
