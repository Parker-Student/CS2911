"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab 4, 041, 2020
- Names: Aidan Waterman, Parker Foord
  -
  -

A simple TCP server/client pair.

The application protocol is a simple format: For each file uploaded, the client first sends four (big-endian) bytes indicating the number of lines as an unsigned binary number.

The client then sends each of the lines, terminated only by '\\n' (an ASCII LF byte).

The server responds with 'A' when it accepts the file.

Then the client can send the next file.


Introduction: (Describe the lab in your own words)

In this lab, we implement the tcp_receive method which allows the user to listen for messages from a sender
and replies to the sender confirming that the message was recieved.


Summary: (Summarize your experience with the lab, what you learned, what you liked, what you disliked, and any suggestions you have for improvement)

Our experience with this lab was not bad, we learned how to use sockets and write to files in python.
We enjoyed debugging our implementation until it worked and disliked trying to decode how the tcp_send method worked.


"""

# import the 'socket' module -- not using 'from socket import *' in order to selectively use items with 'socket.' prefix
import socket
import struct
import time
import sys

# Port number definitions
# (May have to be adjusted if they collide with ports in use by other programs/services.)
TCP_PORT = 12100

# Address to listen on when acting as server.
# The address '' means accept any connection for our 'receive' port from any network interface
# on this system (including 'localhost' loopback connection).
LISTEN_ON_INTERFACE = ''

# Address of the 'other' ('server') host that should be connected to for 'send' operations.
# When connecting on one system, use 'localhost'
# When 'sending' to another system, use its IP address (or DNS name if it has one)
# OTHER_HOST = '155.92.x.x'
OTHER_HOST = 'localhost'


def main():
    """
    Allows user to either send or receive bytes
    """
    # Get chosen operation from the user.
    action = input('Select "(1-TS) tcpsend", or "(2-TR) tcpreceive":')
    # Execute the chosen operation.
    if action in ['1', 'TS', 'ts', 'tcpsend']:
        tcp_send(OTHER_HOST, TCP_PORT)
    elif action in ['2', 'TR', 'tr', 'tcpreceive']:
        tcp_receive(TCP_PORT)
    else:
        print('Unknown action: "{0}"'.format(action))


def tcp_send(server_host, server_port):
    """
    - Send multiple messages over a TCP connection to a designated host/port
    - Receive a one-character response from the 'server'
    - Print the received response
    - Close the socket
    :param str server_host: name of the server host machine
    :param int server_port: port number on server to send to
    """
    print('tcp_send: dst_host="{0}", dst_port={1}'.format(server_host, server_port))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_host, server_port))

    num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    while num_lines != 0:
        print('Now enter all the lines of your message')
        # This client code does not completely conform to the specification.
        #
        # In it, I only pack one byte of the range, limiting the number of lines this
        # client can send.
        #
        # While writing tcp_receive, you will need to use a different approach to unpack to meet the specification.
        #
        # Feel free to upgrade this code to handle a higher number of lines, too.
        tcp_socket.sendall(b'\x00\x00')
        time.sleep(1)  # Just to mess with your servers. :-)
        tcp_socket.sendall(b'\x00' + bytes((num_lines,)))

        # Enter the lines of the message. Each line will be sent as it is entered.
        for line_num in range(0, num_lines):
            line = input('')
            tcp_socket.sendall(line.encode() + b'\n')

        print('Done sending. Awaiting reply.')
        response = tcp_socket.recv(1)
        if response == b'A':  # Note: == in Python is like .equals in Java
            print('File accepted.')
        else:
            print('Unexpected response:', response)

        num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    tcp_socket.sendall(b'\x00\x00')
    time.sleep(1)  # Just to mess with your servers. :-)  Your code should work with this line here.
    tcp_socket.sendall(b'\x00\x00')
    response = tcp_socket.recv(1)
    if response == b'Q':  # Reminder: == in Python is like .equals in Java
        print('Server closing connection, as expected.')
    else:
        print('Unexpected response:', response)

    tcp_socket.close()


def tcp_receive(listen_port):
    """
    - Listen for a TCP connection on a designated "listening" port
    - Accept the connection, creating a connection socket
    - Print the address and port of the sender
    - Repeat until a zero-length message is received:
      - Receive a message, saving it to a text-file (1.txt for first file, 2.txt for second file, etc.)
      - Send a single-character response 'A' to indicate that the upload was accepted.
    - Send a 'Q' to indicate a zero-length message was received.
    - Close data connection.

    :param int listen_port: Port number on the server to listen on
    :author Parker Foord, Aidan Waterman
    """
    message_count = 0
    print('tcp_receive (server): listen_port={0}'.format(listen_port))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((LISTEN_ON_INTERFACE, listen_port))
    tcp_socket.listen(1)
    (data_socket, address) = tcp_socket.accept()
    print_sender_info(LISTEN_ON_INTERFACE, listen_port)
    read_message(data_socket, message_count)
    close_socket(data_socket)
    close_socket(tcp_socket)


def print_sender_info(listen_interface, listen_port):
    """
    - Prints the known information about the sender
    :param listen_interface:
    :param listen_port:
    :return:
    :author Parker Foord
    """
    print("Listen Interface: " + listen_interface)
    print("Listen Port: " + str(listen_port))


def read_line_count(data_socket):
    """
    - Reads the first 4 bytes of a message to determine the line count
    :param data_socket:
    :return:
    :author Aidan Waterman
    """
    return int.from_bytes(
        next_byte(data_socket) + next_byte(data_socket) + next_byte(data_socket) + next_byte(data_socket), 'big')


def read_message(data_socket, count):
    """
    - Reads the message following the line count
    :param count:
    :param data_socket:
    :return:
    :author Parker Foord
    """
    while True:
        total_lines = read_line_count(data_socket)
        if total_lines == 0:
            confirm_zero(data_socket)
            break
        else:
            lines = 0;
            message = ""
            while lines < total_lines:
                lines += 1
                while True:
                    new_byte = next_byte(data_socket)
                    if new_byte == b'\x0A':
                        message += new_byte.decode("ASCII")
                        break
                    else:
                        message += new_byte.decode("ASCII")
            save_to_file(message, count)
            confirm_message(data_socket)
            count += 1


def confirm_zero(data_socket):
    """
    - Returns the accepted "zero message confirmation"
    :return:
    :author Aidan Waterman
    """
    message = 'Q'
    data_socket.sendall(message.encode())


def save_to_file(message, count):
    """
    - Saves the message to a new file
    :param count:
    :param message:
    :return:
    :author Parker Foord
    """
    print(message)
    filename = str(count) + ".txt"
    text_file = open('C:\\Users\\watermana\\Desktop\\Network Protocols\\Lab 4 Saved Files\\' + filename, 'wt')
    n = text_file.write(message)
    text_file.close()


def confirm_message(data_socket):
    """
    - Returns the accepted "non-zero message confirmation"
    :return:
    :author Aidan Waterman
    """
    message = 'A'
    data_socket.sendall(message.encode())


def close_socket(data_socket):
    """
    :author Parker Foord
    - Closes the current socket
    :return:
    """
    data_socket.close()


def next_byte(data_socket):
    """
    Read the next byte from the socket data_socket.
   
    Read the next byte from the sender, received over the network.
    If the byte has not yet arrived, this method blocks (waits)
      until the byte arrives.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.
   
    :param data_socket: The socket to read from. The data_socket argument should be an open tcp
                        data connection (either a client socket or a server data socket), not a tcp
                        server's listening socket.
    :return: the next byte, as a bytes object with a single byte in it
    """
    return data_socket.recv(1)


# Invoke the main method to run the program.
main()
