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

    opcode, filename, mode = read_request_line(client_socket)
    if opcode == 1:
        block_count = get_file_block_count(filename)
        if block_count != -1:
            # send block 1
            build_response(filename, 1)
            while True:
                opcode, ack_block_number, error_code, error_message = read_ack(client_socket)
                if opcode == 4:
                    if ack_block_number == block_count:
                        break
                    else:
                        build_response(filename, ack_block_number + 1)
                elif opcode == 5:
                    # handle error
                    break
                else:
                    break
        else:
            # send error message
    else:
        # send error message



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
    return client_socket.recvfrom(MAX_UDP_PACKET_SIZE)


def read_request_line(client_socket):
    message = next_message(client_socket)
    opcode =
    filename =
    mode =
    return opcode, filename, mode


def read_ack(client_socket):
    message = next_message(client_socket)
    opcode =
    block_number =
    error_code =
    error_message =
    return opcode, block_number, error_code, error_message


def build_response(filename, block_number):
    response = b'\x00\x03' + block_number.encode('ASCII') + get_file_block(filename, block_number)
    return response


"""
Read request line
    # get the proper file
    # build response message
    # send response back to user
What We Need To Do:
Build messages
Send messages
Read from client
Parse Message
"""
main()
