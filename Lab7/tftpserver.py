"""
  - CS2911 - 021
  - Fall 2021
  - Lab 7
  - Names: Parker Foord and Aidan Waterman
  - 

A Trivial File Transfer Protocol Server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

# import modules -- not using "from socket import *" in order to selectively use items with "socket." prefix
import socket
import os
import math

# Helpful constants used by TFTP
TFTP_PORT = 69
TFTP_BLOCK_SIZE = 512
MAX_UDP_PACKET_SIZE = 65536


def main():
    """
    Processes a single TFTP request
    """

    client_socket = socket_setup()

    print("Server is ready to receive a request")

    ####################################################
    # Your code starts here                            #
    #   Be sure to design and implement additional     #
    #   functions as needed                            #
    ####################################################

    opcode, filename, mode, address = read_request_line(client_socket)
    if opcode == 1:
        block_count = get_file_block_count(filename)
        if block_count != -1:
            client_socket.sendto(build_response(filename, 1), address)
            while True:
                opcode, ack_block_number, error_code, error_message = read_ack(client_socket)
                if opcode == 4:
                    if ack_block_number == block_count:
                        break
                    else:
                        next_block = ack_block_number + 1
                        print(ack_block_number)
                        client_socket.sendto(build_response(filename, next_block), address)
                elif opcode == 5:
                    print(error_code + " error: " + error_message)
                    break
        else:
            client_socket.sendto(build_error(b'\x00\x01', "File not found"), address)
    else:
        client_socket.sendto(build_error(b'\x00\x04', "Only file reading currently supported"), address)



    ####################################################
    # Your code ends here                              #
    ####################################################

    client_socket.close()


def get_file_block_count(filename):
    """
    Determines the number of TFTP blocks for the given file
    :param filename: THe name of the file
    :return: The number of TFTP blocks for the file or -1 if the file does not exist
    """
    try:
        # Use the OS call to get the file size
        #   This function throws an exception if the file doesn't exist
        file_size = os.stat(filename).st_size
        return math.ceil(file_size / TFTP_BLOCK_SIZE)
    except:
        return -1


def get_file_block(filename, block_number):
    """
    Get the file block data for the given file and block number
    :param filename: The name of the file to read
    :param block_number: The block number (1 based)
    :return: The data contents (as a bytes object) of the file block
    """
    file = open(filename, 'rb')
    block_byte_offset = (block_number-1) * TFTP_BLOCK_SIZE
    file.seek(block_byte_offset)
    block_data = file.read(TFTP_BLOCK_SIZE)
    file.close()
    return block_data


def put_file_block(filename, block_data, block_number):
    """
    Writes a block of data to the given file
    :param filename: The name of the file to save the block to
    :param block_data: The bytes object containing the block data
    :param block_number: The block number (1 based)
    :return: Nothing
    """
    file = open(filename, 'wb')
    block_byte_offset = (block_number-1) * TFTP_BLOCK_SIZE
    file.seek(block_byte_offset)
    file.write(block_data)
    file.close()


def socket_setup():
    """
    Sets up a UDP socket to listen on the TFTP port
    :return: The created socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', TFTP_PORT))
    return s


####################################################
# Write additional helper functions starting here  #
####################################################

def next_message(client_socket):
    """
    Receives the next message on the socket
    :param client_socket:
    :return: message
    :author: Aidan Waterman
    """
    return client_socket.recvfrom(MAX_UDP_PACKET_SIZE)


def read_request_line(client_socket):
    """
    Parses the request line of the message
    :param client_socket:
    :return: opcode, filename, mode, and address
    :author: Parker Foord
    """
    message, address = next_message(client_socket)
    opcode = message[0: 2]
    message = str(message.split(opcode)[1])
    opcode = int.from_bytes(opcode, 'big')
    parsed = message.split("\\x00")
    filename = parsed[0].removeprefix("b'")
    mode = parsed[1]
    return opcode, filename, mode, address


def read_ack(client_socket):
    """
    Parses the acknowledgement message
    :param client_socket:
    :return: opcode, block number recieved, error code, error message
    :author: Aidan Waterman
    """
    message = next_message(client_socket)[0]
    block_number = 0
    error_code = -1
    error_message = -1
    opcode = message[0: 2]
    if int.from_bytes(opcode, 'big') == 4:
        block_number = message.split(opcode)[1]
        if block_number == b'':
            block_number = b'\x00\x04'
    elif int.from_bytes(opcode, 'big') == 5:
        error_code = message[2: 4]
        split_code = opcode + error_code
        error_message = str(message.split(split_code)[1])
    return int.from_bytes(opcode, 'big'), int.from_bytes(block_number, 'big'), error_code, error_message


def build_response(filename, block_number):
    """
    Builds a data response to send the user
    :param filename:
    :param block_number:
    :return: message to send
    :author: Aidan Waterman
    """
    response = b'\x00\x03' + block_number.to_bytes(2, 'big') + get_file_block(filename, block_number)
    return response


def build_error(errorcode, message):
    """
    Builds an error response to send the user
    :param errorcode:
    :param message:
    :return: message to send
    :author: Parker Foord
    """
    response = b'\x00\x05' + errorcode + message.encode('ASCII') + b'\x20'
    return response

main()
