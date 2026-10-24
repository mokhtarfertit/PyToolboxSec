import threading
import paramiko #this library for make secure connection
import subprocess

def ssh_command(ip,user,passwd,command):
    client = paramiko.SSHClient()

    #laod known ssh hosts if you want host-key verification
    #cleit.load_host_keys('/home/justin/.ssh/known_hosts')
    
    #for a lab, automatically accept an unknown host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    client.connect(ip,username=user,password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)

        output = ssh_session.recv(1024)
        print(output.decode("utf-8", errors="replace"))

    client.close()

ssh_command("*","*","*","whoami")

