import pyperfmon


print("Start						", time.time())
pm = pyperfmon()

print("Init Class					", time.time())

# remotehost = "remotehost"
# pm.connect(remotehost)
#
# print("Connect remotehost				", time.time())

for i in range(5):
	# print("\ngetCounterObjects:", pm.getCounterObjects())
	# print("\nSystem:", pm.getCounters("System"))
	print("\nSystem\Processor Queue Length", pm.getCounter(r"System\Processor Queue Length"))

	print(pm.getCounter(r"Processor\0\% Processor Time"))
	print(pm.getCounter(r"Processor\1\% Processor Time"))
	print(pm.getCounter(r"Processor\2\% Processor Time"))
	print(pm.getCounter(r"Processor\3\% Processor Time"))
	print(pm.getCounter(r"Processor\4\% Processor Time"))
	print(pm.getCounter(r"Processor\5\% Processor Time"))
	print(pm.getCounter(r"Processor\6\% Processor Time"))
	print(pm.getCounter(r"Processor\7\% Processor Time"))
	print(pm.getCounter(r"Processor\_Total\% Processor Time"))

	print(pm.getCounter(r"Memory\Page Writes/sec"))
	print(pm.getCounter(r"Memory\Page Reads/sec"))
	print(pm.getCounter(r"Memory\Pages/sec"))
	print(pm.getCounter(r"Memory\Cache Bytes"))
	print(pm.getCounter(r"Memory\% Committed Bytes In Use"))
	print(pm.getCounter(r"Memory\Available Bytes"))

	print("Local Counters					", time.time())

	# print(pm.getCounter(r"System\Processor Queue Length", remotehost))
	#
	# print(pm.getCounter(r"Processor\_Total\% Idle Time", remotehost))
	# print(pm.getCounter(r"Processor\0\% Processor Time", remotehost))
	# print(pm.getCounter(r"Processor\1\% Processor Time", remotehost))
	# print(pm.getCounter(r"Processor\2\% Processor Time", remotehost))
	# print(pm.getCounter(r"Processor\3\% Processor Time", remotehost))
	# print(pm.getCounter(r"Processor\_Total\% Processor Time", remotehost))
	#
	# print(pm.getCounter(r"Memory\Page Writes/sec", remotehost))
	# print(pm.getCounter(r"Memory\Page Reads/sec", remotehost))
	# print(pm.getCounter(r"Memory\Pages/sec", remotehost))
	# print(pm.getCounter(r"Memory\Cache Bytes", remotehost))
	# print(pm.getCounter(r"Memory\% Committed Bytes In Use", remotehost))
	# print(pm.getCounter(r"Memory\Available Bytes", remotehost))
	#
	# print("DCDESK01VP Counters				", time.time())

	time.sleep(1)
