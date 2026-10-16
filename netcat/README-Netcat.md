# Python Netcat

A lightweight Python-based networking tool inspired by Netcat a It uses TCP sockets to establish client-server connections and supports sending data, receiving connections, transferring files, and executing commands.

## Features

- **TCP Client:** Connect to a target host and port.
- **TCP Listener:** Listen for incoming TCP connections.
- **Data Transmission:** Send data through a TCP connection.
- **File Upload:** Receive file data and save it to a specified destination.
- **Command Execution:** Execute a specified command and return its output.
- **Interactive Command Shell:** Receive commands from a connected client and return their output.
- **Multithreading:** Handle incoming connections using separate threads.

## Requirements

- Python 3.x
- Standard Python libraries:
  - `socket`
  - `sys`
  - `getopt`
  - `threading`
  - `subprocess`

No third-party Python packages are required.

## Installation

Clone your repository or download the script, then navigate to its directory:

```bash
cd path/to/netcat
```

Run the help command to display the available options:

```bash
python3 netcat.py -h
```

## Command-Line Options

| Option | Description |
|---|---|
| `-h`, `--help` | Display usage information. |
| `-t`, `--target` | Specify the target IP address or hostname. |
| `-p`, `--port` | Specify the TCP port. |
| `-l`, `--listen` | Listen for incoming connections. |
| `-e`, `--execute` | Execute a specified command when a connection arrives. |
| `-c` | Enable an interactive command shell on the listener. |
| `-u`, `--upload` | Specify the destination path for a received file. |

## Usage Examples

### 1. Connect to a TCP Server

Connect to a TCP service running on localhost at port `9001`:

```bash
python3 netcat.py -t 127.0.0.1 -p 9001
```

The program reads input from standard input and sends it to the target. It then displays the received response.

### 2. Start a TCP Listener

Listen for incoming TCP connections on port `9001`:

```bash
python3 netcat.py -t 0.0.0.0 -p 9001 -l
```

`0.0.0.0` means the server binds to all available network interfaces. Use a specific interface address when you want to restrict which interface accepts connections.

### 3. Enable an Interactive Command Shell

On a controlled test machine, start the listener with command-shell support:

```bash
python3 netcat.py -t 127.0.0.1 -p 9001 -l -c
```

When a client connects, the listener displays a command prompt and executes received commands, returning their output to the client.

**Security warning:** This feature allows remote command execution. Use it only in an isolated lab or on systems you own or are explicitly authorized to test. Do not expose it to untrusted networks.

### 4. Execute a Single Command

Run a command when a client connects:

```bash
python3 netcat.py -t 127.0.0.1 -p 9001 -l -e "whoami"
```

The listener executes the specified command and sends the output to the connected client.

### 5. Receive a File

Specify the destination where incoming file data should be saved:

```bash
python3 netcat.py -t 127.0.0.1 -p 9001 -l -u received_file.bin
```

The listener receives data until the client closes its sending connection, then writes the received bytes to `received_file.bin`.

**Important:** The current implementation treats the received stream as file content until the connection closes. It does not implement a file-size header, integrity verification, or a separate upload protocol.

### 6. Send Data from Standard Input

Send text to a TCP service:

```bash
echo "Hello from Python Netcat" | python3 netcat.py -t 127.0.0.1 -p 9001
```

This reads the piped text from standard input and sends it to the target.

## How It Works

The tool has four main components:

- **Client (`client_sender`)** — Establishes a TCP connection, sends data, and reads responses.
- **Listener (`server_loop`)** — Binds to a host and port, listens for connections, and starts a thread for each accepted connection.
- **Connection Handler (`client_handler`)** — Handles file uploads, command execution, and interactive shell requests according to the configured options.
- **Command Runner (`run_command`)** — Runs a system command and captures its output.

The program uses TCP sockets through Python's `socket` module and handles connections with `threading`.

## Current Limitations

- The implementation is a learning project and is not a production-ready networking utility.
- The port is parsed as an integer, but the target defaults and option combinations are not fully validated.
- The client response-reading logic may wait indefinitely when a server keeps the connection open.
- File transfers have no size limit, authentication, encryption, or integrity checks.
- The command execution features use `subprocess.check_output()` with `shell=True`, which can introduce command-injection risks when handling untrusted input.
- The server does not implement authentication or access control.
- The `-e` option executes a command, not an arbitrary executable file in the way its help text may imply.
- The `-c` option is internally parsed as `--commandshell`; the help text should be updated to match the supported option name.

## Troubleshooting

**Connection refused**

Make sure the target service is listening on the specified port and that the address and port are correct.

**Address already in use**

Another process may already be using the selected port. Choose another port or stop the existing process.

**Permission denied**

Check the permissions for the selected destination path and whether the process is allowed to bind to the requested port.

**No response from the server**

Verify that the server is expecting the data you send and that both sides use a compatible protocol.

## Disclaimer

This project is intended for educational purposes, networking practice, and authorized cybersecurity testing. Use it only on systems and networks you own or have explicit permission to test. Remote command execution and file-transfer capabilities can create serious security risks if exposed improperly.

## License

Add a license file if you intend to distribute this project publicly. Until a license is specified, all rights remain with the copyright holder.
