# pyperfmon
Python Module for reading performance monitor counters from local and remote windows machines

This module is designed to make querying performance monitor counters in python easy for both local and remote machines.

There is only one dependancy, the [WMI](https://github.com/tjguk/wmi/blob/master/readme.rst) module that is used to connect to the machine to be monitored and query the counters.

Only one instance needs to be created and can be used to connect to many machines, even when using different credentials for each machine.

## Using this module

First import the module and create an instance
```python
import pyperfmon

pm = pyperfmon()

```

### Connecting
If the windows domain account you are running this code with, has sufficient privileges to connect to and view performance monitor counters on the remote machine that you want to monitor, then calling connect is optional, it will be triggered automatically when you call another function. However it may be advantageous to call the connect function to improve the performance of your code when retrieving the first counter.

```python
pm.connect("hostname")
```

If you need different credentials to connect to another machine then you you will need to call connect with that user account, using the optional username and password arguments, this is not optional as this is the only way you can provide a different user account when connecting. e.g:

```python
pm.connect("server1", r"domain\user1", "password1")
pm.connect("server2", "domain\\user1", "password1")
pm.connect("server3.dns.siffix", "localuser", "password2")
pm.connect("192.168.1.13", r"domain2\user13", "password13")
```

### Querying performance monitor counters
Querying performance monitor counters is done with the `getCounter` function, which takes 1 or 2 arguments, the first argument, the performance counter is mandatory, the second is the hostname you want to read the counter from. If the optional hostname argument is not used the counter will be read from the localhost.

There are 2 options when specifying the counter, the first is the single instance counters where you specify "Object\\counter name" e.g.
```python
print(pm.getCounter(r"Memory\Pages/sec"))
```

The second is the multi-instance counters where you specify "Object\\instance\\counter name" e.g.
```python
print(pm.getCounter(r"Processor\0\% Processor Time"))
print(pm.getCounter(r"Processor\1\% Processor Time"))
print(pm.getCounter(r"Processor\2\% Processor Time"))
print(pm.getCounter(r"Processor\3\% Processor Time"))
print(pm.getCounter(r"Processor\_Total\% Processor Time"))
```

The same examples from when monitoring multiple hosts

```python
print(pm.getCounter(r"Memory\Pages/sec", "server1"))
print(pm.getCounter(r"Processor\0\% Processor Time", "server1"))
print(pm.getCounter(r"Processor\1\% Processor Time", "server1"))
print(pm.getCounter(r"Processor\2\% Processor Time", "server1"))
print(pm.getCounter(r"Processor\3\% Processor Time", "server1"))
print(pm.getCounter(r"Processor\_Total\% Processor Time", "server1"))

print(pm.getCounter(r"Memory\Pages/sec", "server2"))
print(pm.getCounter(r"Processor\0\% Processor Time", "server2"))
print(pm.getCounter(r"Processor\1\% Processor Time", "server2"))
print(pm.getCounter(r"Processor\2\% Processor Time", "server2"))
print(pm.getCounter(r"Processor\3\% Processor Time", "server2"))
print(pm.getCounter(r"Processor\_Total\% Processor Time", "server2"))
```

### Querying available performance monitor counters

As the performance monitor counters names are localised and you may not know the localised name used on the server you want to monitor or you may want to check first if the counters you are interested is available on the remote machine. for this we provide these 2 utility function
- `getCounterObjects` - returns a list of objects on windows machine being monitored. e.g.
```python
print(pm.getCounterObjects("server1"))
```
- `getCounters` - returns a list of counters available for a specific object on the windows machine being monitored. e.g.
```python
print(pm.getCounters("System", "server1"))
```

Again with these functions the hostname is optional, if omitted the localhost will be queried.


## Installing

```
pip install pyperfmons
```
