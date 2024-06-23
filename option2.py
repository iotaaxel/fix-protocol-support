```python
import socket
import struct
import time

class FIXSession:
    def __init__(self, host, port, sender_comp_id, target_comp_id):
        self.host = host
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.seq_num = 1

    def send_message(self, msg_type, msg_data):
        msg = f"8=FIX.4.2|9={len(msg_data)}|35={msg_type}|49={self.sender_comp_id}|56={self.target_comp_id}|34={self.seq_num}|52={int(time.time())}|{msg_data}"
        self.socket.sendall(msg.encode())
        self.seq_num += 1

    def receive_message(self):
        msg = self.socket.recv(1024)
        if not msg:
            return None
        msg = msg.decode()
        fields = msg.split("|")
        msg_type = fields[3].split("=")[1]
        return msg_type, fields

    def logon(self):
        self.send_message("A", "98=0|108=30")

    def logout(self):
        self.send_message("5", "")

    def heartbeat(self):
        self.send_message("0", "")

    def test_request(self):
        self.send_message("1", "112=TEST")

    def close(self):
        self.socket.close()

class FIXApplication:
    def __init__(self, session):
        self.session = session

    def on_logon(self, msg):
        print("Logged on")

    def on_logout(self, msg):
        print("Logged out")

    def on_heartbeat(self, msg):
        print("Heartbeat received")

    def on_test_request(self, msg):
        print("Test request received")

    def on_message(self, msg_type, fields):
        if msg_type == "A":
            self.on_logon(fields)
        elif msg_type == "5":
            self.on_logout(fields)
        elif msg_type == "0":
            self.on_heartbeat(fields)
        elif msg_type == "1":
            self.on_test_request(fields)
        else:
            print(f"Unknown message type: {msg_type}")

def main():
    session = FIXSession("localhost", 9876, "SENDER", "TARGET")
    app = FIXApplication(session)
    session.logon()
    while True:
        msg_type, fields = session.receive_message()
        if msg_type is None:
            break
        app.on_message(msg_type, fields)
    session.logout()
    session.close()

if __name__ == "__main__":
    main()
