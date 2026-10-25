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
            received_command = data.decode(
                "utf-8",
                errors="replace"
            ).strip()

            if received_command == "exit":
                break

            # For demonstration, only handle known commands.
            commands = {
                "whoami": ["whoami"],
                "hostname": ["hostname"],
                "ipconfig": ["ipconfig"]
            }

            if received_command not in commands:
                ssh_session.send(
                    b"Command not supported"
                )
                continue

            try:
                result = subprocess.run(
                    commands[received_command],
                    capture_output=True,
                    text=True,
                    check=False
                )

                output = result.stdout + result.stderr

                # Python 3: string -> bytes
                ssh_session.send(
                    output.encode("utf-8")
                )

            except Exception as e:
                error = str(e)

                ssh_session.send(
                    error.encode("utf-8")
                )

    client.close()


ssh_command(
    "*",
    "*",
    "*",
    "ClientConnected"
)