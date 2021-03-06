"""
  - CS2911 - 021
  - Fall 2021
  - Lab 6
  - Names: Parker Foord and Aidan Waterman
  - 
  - 

An HTTP server

Introduction: (Describe the lab in your own words)
    The goal of this lab is to handle all possible requests that the server receives and if the request is a valid
    request for a resource that we have downloaded, return a response containing the resource, otherwise return a message
    containing 404 or 400 status codes.

Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)
    This lab was not too difficult once the framework of lab 5 was properly built. This lab was nearly the exact opposite
    of the previous lab and that helped a lot because we knew exactly what to build without doing too much more research.
    Throughout this lab, we learned when to encode and decode data that is either being sent or received. We also learned
    to debug using wireshark more effectively.

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
        resource = dictionary['Request'].split(" ")[1]
        if resource == "/" or resource == "/index.html" or resource == "/msoe.png" or resource == "/styles.css":
            res = 0
            if resource == "/":
                res = 1
            elif resource == "/index.html":
                res = 2
            elif resource == "/msoe.png":
                res = 3
            elif resource == "/styles.css":
                res = 4
            response = build_response(200, res)
        else:
            response = build_response(404, 0)
    else:
        response = build_response(400, 0)
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
    :author: Aidan Waterman
    """
    if "Host" in dictionary.keys() and "Request" in dictionary.keys():
        return True
    else:
        return False


def build_response(status_code, request):
    """
    builds a bytes object containing the response message
    :param status_code:
    :param request:
    :return: message
    :author: Aidan Waterman, Parker Foord
    """
    timestamp = datetime.datetime.utcnow()
    time_string = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    body = b''
    response = {"Status": [], "Date": time_string, "Content-Length": [], "Content-Type": [], "Connection": "Closed"}
    if status_code == 200:
        response["Status"] = "HTTP/1.1 200 OK".encode('ASCII')
        if request == 4:
            resource = "./Lab6Resources/styles.css"
        elif request == 3:
            resource = "./Lab6Resources/msoe.png"
        elif request == 1 or 2:
            resource = "./Lab6Resources/index.html"
        response["Content-Type"] = get_mime_type(resource)
        response["Content-Length"] = str(get_file_size(resource))
        file = open(resource, "rb")
        byte = file.read(1)
        while byte:
            body += byte
            byte = file.read(1)
        file.close()
    elif status_code == 400:
        response["Status"] = "HTTP/1.1 400 Bad Request".encode('ASCII')
    elif status_code == 404:
        response["Status"] = "HTTP/1.1 404 Not Found".encode('ASCII')
    else:
        response = "Error".encode('ASCII')
    message = response["Status"]
    message += b'\x0D\x0A'
    if status_code == 200:
        for key, value in response.items():
            if key != "Status":
                message += key.encode('ASCII')
                message += ": ".encode('ASCII')
                message += str(value).encode('ASCII')
                message += b'\x0D\x0A'
    elif status_code == 400 or status_code == 404:
        message += "Date".encode('ASCII')
        message += ": ".encode('ASCII')
        message += str(response["Date"]).encode('ASCII')
        message += b'\x0D\x0A'
        message += "Connection".encode('ASCII')
        message += ": ".encode('ASCII')
        message += str(response["Connection"]).encode('ASCII')
        message += b'\x0D\x0A'
    message += b'\x0D\x0A'
    message += body
    return message


def send_response(request_socket, response):
    """
    Sends the response message on the given socket
    :param request_socket:
    :param response:
    :return:
    :author: Parker Foord
    """
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
