"""
  - CS2911 - 021
  - Fall 2021
  - Lab 6
  - Names: Parker Foord and Aidan Waterman
  - 
  - 

An HTTP server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

import socket
import re
import threading
import os
import mimetypes
import datetime


def main():
    """ Start the server """
    http_server_setup(8080)


def http_server_setup(port):
    """
    Start the HTTP server
    - Open the listening socket
    - Accept connections and spawn processes to handle requests

    :param port: listening port number
    """

    num_connections = 10
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_address = ('', port)
    server_socket.bind(listen_address)
    server_socket.listen(num_connections)
    try:
        while True:
            request_socket, request_address = server_socket.accept()
            print('connection from {0} {1}'.format(request_address[0], request_address[1]))
            # Create a new thread, and set up the handle_request method and its argument (in a tuple)
            request_handler = threading.Thread(target=handle_request, args=(request_socket,))
            # Start the request handler thread.
            request_handler.start()
            # Just for information, display the running threads (including this main one)
            print('threads: ', threading.enumerate())
    # Set up so a Ctrl-C should terminate the server; this may have some problems on Windows
    except KeyboardInterrupt:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())
        server_socket.close()


def handle_request(request_socket):
    """
    Handle a single HTTP request, running on a newly started thread.

    Closes request socket after sending response.

    Should include a response header indicating NO persistent connection

    :param request_socket: socket representing TCP connection from the HTTP client_socket
    :return: None
    """

    dictionary = parse_request(request_socket)
    if is_valid_request(dictionary):
        resource = dictionary ['Request'].split(" ")[1]
        if resource == "/" or "/index.html" or "/msoe.png" or "/styles.css":
            response = build_response(200, resource)
        else:
            build_response(404)
    else:
        response = build_response(400)
    send_response(request_socket, response)
    request_socket.close()


def parse_request(request_socket):
    """
    Parses the request and stores the key:value pairs in a dictionary
    :param request_socket:
    :return: dictionary of key:value pairs
    :Author: Parker Foord
    """
    request_line = next_line(request_socket)
    dictionary = {}
    while True:
        line = next_line(request_socket)
        if line == b'\x0D\x0A':
            dictionary["Request"] = request_line.decode('ASCII')
            return dictionary

        else:
            split_line = line.split(": ".encode('ASCII'))
            key = split_line[0]
            value = split_line[1]
            dictionary[key.decode('ASCII')] = value.decode('ASCII')


def is_valid_request(dictionary):
    """
    Checks if the dictionary contains a request and host line
    :param dictionary:
    :return: a boolean representing if the request is valid or not
    """
    if "Host" in dictionary.keys() and "Request" in dictionary.keys():
        return True
    else:
        return False


def build_response(status_code, *request):
    """

    :param status_code:
    :param request:
    :return:
    """
    timestamp = datetime.datetime.utcnow()
    time_string = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    response = {"Status": [], "Date": time_string, "Content-Length": [], "Content-Type": [], "Connection": "Closed"}
    if status_code == 200:
        response["Status"] = "HTTP/1.1 200 OK".encode('ASCII')
        if request == "/" or "/index.html":
            resource = "./Lab6Resources/index.html"
        elif request == "/msoe.png":
            resource = "./Lab6Resources/msoe.png"
        elif request == "/styles.css":
            resource = "./Lab6Resources/styles.css"
        response["Content-Type"] = get_mime_type(resource)
        response["Content-Length"] = str(get_file_size(resource))
        body = open(resource, "rb").read()
    elif status_code == 400:
        response["Status"] = "HTTP/1.1 400 Bad Request".encode('ASCII')
    elif status_code == 404:
        response["Status"] = "HTTP/1.1 404 Not Found".encode('ASCII')
    else:
        response = "Error".encode('ASCII')
    message = response["Status"]
    for key, value in response.items():
        message += key.encode('ASCII')
        message += str(value).encode('ASCII')
        message += b'\x0D\x0A'
    message += body
    return message


def send_response(request_socket, response):
    request_socket.sendall(response)


def next_line(data_socket):
    """
    Reads bytes until a new line is found
    :param data_socket:
    :return: Byte object containing a single line of data
    :Author: Aidan Waterman
    """
    line = b''
    while b'\x0D\x0A' not in line:
        line += next_byte(data_socket)
    return line


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


# ** Do not modify code below this line.  You should add additional helper methods above this line.

# Utility functions
# You may use these functions to simplify your code.


def get_mime_type(file_path):
    """
    Try to guess the MIME type of a file (resource), given its path (primarily its file extension)

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
             Otherwise, None
    :rtype: int or None
    """

    mime_type_and_encoding = mimetypes.guess_type(file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


def get_file_size(file_path):
    """
    Try to get the size of a file (resource) as number of bytes, given its path

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If file_path designates a normal file, an integer value representing the the file size in bytes
             Otherwise (no such file, or path is not a file), None
    :rtype: int or None
    """

    # Initially, assume file does not exist
    file_size = None
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
    return file_size


main()

# Replace this line with your comments on the lab
