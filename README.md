<h1 align="center">local chat</h1>

<p align="center">
    <img src="https://img.shields.io/badge/python-v3.10.7-blue" alt="python version">
    <img src="https://img.shields.io/pypi/v/cryptography/38.0.1?color=green&label=cryptography" alt="cryptography version">
    <img src="https://img.shields.io/pypi/v/openpyxl/3.0.10?color=green&label=openpyxl" alt="openpyxl version">
    <img src="https://img.shields.io/pypi/v/pyfiglet/0.7?color=green&label=pyfiglet" alt="pyfiglet version">
    <img src="https://img.shields.io/pypi/v/rich/12.6.0?color=green&label=rich" alt="rich version">
</p>

<p align="center">
    <img src="https://img.shields.io/github/forks/peymone/local_chat?style=social" alt="Forks">
    <img src="https://img.shields.io/github/stars/peymone/local_chat?style=social" alt="Stars">
    <img src="https://img.shields.io/github/downloads/peymone/local_chat/total?style=social" alt="Downloads">
</p>

##About

_This local chat allows you to send secure messages, using symmetric encryption, to users on the same local network. For the application to work, you need to start the server and transfer the data necessary for connection through a secure source to prevent interception of the first insecure messages._

---
##Istallation

1. _Remove everything from the project except the role you are interested in: server or client_
2. _Install python from [offisial site](https://www.python.org/downloads/)_
3. _Open terminal in your role directory and type `pip install -r requirements.txt`_

---

###Program launch for server:

* _Open terminal in your role directory (cd path/server)_
* _Type `python server.py [port]`_
* _Share data with the client: ip and port, acess_key and offset_
* _Type `-help` for show all available commands_
* _Type anything else for broadcast to clients_

###Program launch for client:

* _Open terminal in your role directory (cd path/client)_
* _Type `python client.py [server_ip] [server_port]`_
* _Follow the program instruction_

> _Good night and good chat! xD_

