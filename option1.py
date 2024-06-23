import socket
import struct
import time

class FIXConnection:
    def __init__(self, host, port, sender_comp_id, target_comp_id):
        self.host = host
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.msg_seq_num = 1

    def send_message(self, msg_type, fields):
        msg = f"8=FIX.4.2|9={len(fields)}|35={msg_type}|49={self.sender_comp_id}|56={self.target_comp_id}|"
        for field in fields:
            msg += f"{field[0]}={field[1]}|"
        msg += f"10={self.calculate_checksum(msg)}|"
        self.socket.sendall(msg.encode())
        self.msg_seq_num += 1

    def receive_message(self):
        msg = ""
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            msg += data.decode()
            if msg[-1] == "|":
                break
        fields = msg.split("|")
        return {field.split("=")[0]: field.split("=")[1] for field in fields}

    def calculate_checksum(self, msg):
        checksum = 0
        for char in msg:
            checksum += ord(char)
        return checksum % 256

    def heartbeat(self):
        self.send_message("0", [])

    def logon(self):
        self.send_message("A", [
            ("34", str(self.msg_seq_num)),
            ("52", str(int(time.time()))),
            ("98", "0"),
            ("108", "30")
        ])

    def logout(self):
        self.send_message("5", [
            ("34", str(self.msg_seq_num)),
            ("52", str(int(time.time())))
        ])

    def close(self):
        self.socket.close()
