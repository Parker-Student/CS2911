"""
- CS2911 - 021
- Fall 2021
- Lab 5
- Names: Parker Foord and Aidan Waterman
  - 
  - 

An HTTP client

Introduction: In this lab we are going to act as an HTTP client in order to save a web resource.
This will consist of writing a python script that:
creates a tcp socket
read bytes from the tcp socket
{
    response header
        response line
        key value lines
        blank line
    response body
       if chunking
       {
        size
        crlf
        data
        0
        crlf
        crlf
        }

        else
        {
        size
        crlf
        message
        crlf
        crlf
        }

interprets the bytes
parses the message
}

save to file
return message

make and build an http request




Summary: (Summarize your experience with the lab, what you learned, what you liked, what you
   disliked, and any suggestions you have for improvement)





"""

# import the "socket" module -- not using "from socket import *" in order to selectively use items
# with "socket." prefix
import socket

# import the "regular expressions" module
import re


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('http://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('http://www.httpvshttps.com/', 'index.html')

    # HTTPS example. (Just for fun.)
    # get_http_resource('https://www.httpvshttps.com/', 'https_index.html')

    # If you find fun examples of chunked or Content-Length pages, please share them with us!


def get_http_resource(url, file_name):
    """
    Get an HTTP resource from a server
           Parse the URL and call function to actually make the request.

    :param url: full URL of the resource to get
    :param file_name: name of file in which to store the retrieved resource

    (do not modify this function)
    """

    # Parse the URL into its component parts using a regular expression.
    if url.startswith('https://'):
        use_https = True
        protocol = 'https'
        default_port = 443
    else:
        use_https = False
        protocol = 'http'
        default_port = 80
    url_match = re.search(protocol + '://([^/:]*)(:\d*)?(/.*)', url)
    url_match_groups = url_match.groups() if url_match else []
    #    print 'url_match_groups=',url_match_groups
    if len(url_match_groups) == 3:
        host_name = url_match_groups[0]
        host_port = int(url_match_groups[1][1:]) if url_match_groups[1] else default_port
        host_resource = url_match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'.
              format(host_name, host_port, host_resource))
        status_string = do_http_exchange(use_https, host_name.encode(), host_port,
                                         host_resource.encode(), file_name)
        print('get_http_resource: URL="{0}", status="{1}"'.format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')


def do_http_exchange(use_https, host, port, resource, file_name):
    """
    Get an HTTP resource from a server

    :param use_https: True if HTTPS should be used. False if just HTTP should be used.
           You can ignore this argument unless you choose to implement the just-for-fun part of the
           lab.
    :param bytes host: the ASCII domain name or IP address of the server machine (i.e., host) to
           connect to
    :param int port: port number to connect to on server host
    :param bytes resource: the ASCII path/name of resource to get. This is everything in the URL
           after the domain name, including the first /.
    :param file_name: string (str) containing name of file in which to store the retrieved resource
    :return: the status code
    :rtype: int
    """
    (data_socket, address) = create_socket(port)
    send_request(data_socket)
    header = get_header(data_socket)
    if (is_chunking(header)):
        while True:
            size = read_size(data_socket)
            if (size == 0):
                break
            read_chunked_message(data_socket)
    elif (not (is_chunking(header))):
        size = read_size(data_socket)
        read_message(size)
    else:
        # error message
        return 500

    return send_return_message()  # Replace this "server error" with the actual status code


# Define additional functions here as necessary
# Don't forget docstrings and :author: tags


def create_socket(port):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', port))
    tcp_socket.listen(1)
    return tcp_socket.accept()


def send_request(data_socket):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """


def get_header(data_socket):
    """

    :return: header lines as a bytes object
    :author: Parker Foord, Aidan Waterman
    """
    while True:
        new_byte = next_byte(data_socket)
        header_bytes = + new_byte
        if (new_byte == b'\xCR\xLF' and old_byte == b'\xCR\xLF'):
            break
        old_byte = new_byte
        

    # read through the response line, grab the status value
    read_key_value_lines()
    # read blank line


def read_key_value_lines(data_socket):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """


def read_chunked_message(data_socket):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """


def read_message(data_socket):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """
    while True:
        new_byte = next_byte()


def save_to_file(file_name, content):
    """
    The method saves the message contents to a given filename
    :author: Parker Foord
    """

    with open(file_name, 'w') as file:
        file.write(content)


def send_return_message(data_socket):
    """

    :return:
    :author: Parker Foord, Aidan Waterman
    """


def read_size(data_socket):
    """
    Reads the next bytes in a response until it runs into a new line, these bytes are the size
    :return: size of the message following
    :author: Aidan Waterman
    """
    size = b'\x00'
    while True:
        new_byte = next_byte(data_socket)
        if (new_byte == b'\x0d'):
            next_byte(data_socket)
            return size
        else:
            size += new_byte


def is_chunking(header):
    """

    :return:
    """
    # read through bytes until it finds the chunking and returns true or false



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


main()
