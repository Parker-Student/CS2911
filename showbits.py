import warnings
import sys

def bits(v, numbits=None):
    """
    Display the bits used to store an object
    :param v: the value to display the bits of
    :param numbits: the number of bits to display. Only used for int objects. bytes objects
                    always show the exact bits stored, and int objects default to
                    not showing any leading zeros.
    """

    _check_version()
    if type(v) is bytes:
        if numbits:
            warnings.warn('Ignoring provided argument numbits = {} while formatting bytes object'.format(numbits))
        hexstring = _bits_bytes(v)
    elif type(v) is str:
        if numbits:
            warnings.warn('Ignoring provided argument numbits = {} while formatting str object'.format(numbits))
        hexstring = _bits_str(v)
    elif type(v) is int:
        hexstring = _bits_int(v, numbits)
    else:
        raise TypeError('display_bits can only display bytes, str, or int objects')
    print(hexstring)


def _bits_bytes(bytes):
    """
    Internal implementation of bits() for bytes objects
    :param bytes: the bytes object to display the bits of
    :return: A string with an ASCII '0' or '1' for each bit.
            (An ASCII binary string)
    """

    s = ''
    for b in bytes:
        s += ' ' + _bits_int(b, numbits=8)
    return s[1:] # Drop initial space


def _bits_str(s):
    """
    Internal implementatino of bits() for it objects
    :param s: the string to display the bits of
    :return: A string with an ASCII '0' or '1' for each bit
            (An ASCII binary string)
    """
    display = ''
    for c in s:
        display += '\n' + _bits_int(ord(c),21)
    return display[1:] # Drop initial \n


def _bits_int(v, numbits=None):
    """
    Internal implementation of bits() for int objects
    :param v: the int value to display in bits
    :param numbits: The number of bits to display. Defaults to not showing any leading zeros.
    :return: A string with an ASCII '0' or '1' for each bit.
            (An ASCII binary string)
    """

    if numbits and 2**numbits-1 < v:
        raise ValueError('Cannot store '+str(v)+' in '+str(numbits)+' bits')

    if numbits:
        s = "{:0{digits}b}".format(v,digits=str(numbits))
    else:
        s = "{:b}".format(v)

    return _break(s,8) # Break into groups of 8 bits


def shorthand(v, numplaces=None):
    """
    Display the bits used to store an object in hexadecimal shorthand
    :param v: The value to display the bits of in hexadecimal shorthand
    :param numplaces: The number of hexadecimal places (digits) to display.
                      e.g. 0x1ef8 has four hexadecimal places.
                      Only used for int objects. bytes objects always display
                      2 hexadecimal digits for each byte.  int objects default
                      to showing all hexadecimal places without any leading zeros.
    """

    _check_version()
    if type(v) is bytes:
        if numplaces:
            warnings.warn('Ignoring provided argument numbits = {} while formatting bytes object'.format(numplaces))
        hexstring = _shorthand_bytes(v)
    elif type(v) is str:
        if numplaces:
            warnings.warn('Ignoring provided argument numbits = {} while formatting str object'.format(numplaces))
        hexstring = _shorthand_str(v)
    elif type(v) is int:
        hexstring = _shorthand_int(v, numplaces)
    else:
        raise TypeError('display_bits can only display bytes, str, or int objects')
    print(hexstring)


def _shorthand_bytes(bytes):
    """
    Internal implementation of shorthand() for bytes objects
    :param bytes: The bytes object to in hexadecimal shorthand
    :return: A string object holding a single ASCII character for each place.
             e.g., for 0x1ef8, returns '1ef8'
             (An ASCII hexadecimal string)
    """

    s = ''
    for b in bytes:
        s += ' ' + _shorthand_int(b, numplaces=2)
    return s[1:] # Drop initial space


def _shorthand_str(s):
    """
    Internal implementation of shorthand() for str objects
    :param s: String to show shorthand of
    :return: ASCII hexadecimal string: A string where each ASCII
             characters stores a hexadecimal digit.
    """
    display = ''
    for c in s:
        display += '\n' + _shorthand_int(ord(c),6)
    return display[1:] # Drop initial \n


def _shorthand_int(v, numplaces=None):
    """
    Internal implementation of the shorthand() for int objects
    :param v: The int value to display the bits of in hexadecimal shorthand
    :param numplaces: The number of hexadecimal places (digits) to display.
                      e.g. 0x1ef8 has four hexadecimal places.
                      int objects default to showing all hexadecimal places
                      without any leading zeros.
    :return: A string object holding a single ASCII character for each place.
             e.g., for 0x1ef8, returns '1ef8'
             (An ASCII hexadecimal string)
    """
    if numplaces and 2**(numplaces*4)-1 < v:
        raise ValueError('Cannot store ' + str(v) +' in ' + str(numplaces) + ' hex digits')

    if numplaces:
        s = "{:0{digits}x}".format(v,digits=str(numplaces))
    else:
        s = "{:x}".format(v)

    return _break(s,2) # Break into bytes (2 hex digits each)


def _break(bitstring,groupsize):
    """
    Break a binary string into groups of groupsize digits.
    For example, _break('1100001111',4) returns '11 0000 1111'
    :param bitstring: The ASCII binary string to break into groups
    :param groupsize: The number of bits to group together in each group
    :return: A string with spaces inserted between each group.
    """
    broken = ''
    for i in range(len(bitstring)-groupsize,-1,-groupsize):
        broken = bitstring[i:i+groupsize] + ' ' + broken
    if len(bitstring)%groupsize > 0: # Avoid adding space before empty left-most group
        broken = bitstring[0:len(bitstring)%groupsize] + ' ' + broken
    return broken[:-1] # Drop right-most space


def _check_version():
    """
    Check that the code is being run with the right version of Python
    :raises: RuntimeError if Python 2 is used.
    """
    if sys.version_info < (3,):
        raise RuntimeError('This course requires Python 3. Please uninstall Python 2 and install Python 3 in its place.'
                           '(If you need Python 2 for a different class or project, please talk to me.)')


def _tests():
    """
    Internal tests. These are run if the module is executed as a stand-alone script.
    """
    print("shorthand(b'\\x0a\\x0d')")
    shorthand(b'\x0a\x0d')
    print("bits(b'A\\r\\n')")
    bits(b'A\r\n')
    print("bits(b'\\x0a\\x0d')")
    bits(b'\x0a\x0d')
    print("shorthand(15)")
    shorthand(15)
    print("shorthand(1000)")
    shorthand(1000)
    print("bits(15)")
    bits(15)
    print("bits(1000)")
    bits(1000)
    print("shorthand('A\\r\\n')")
    shorthand('A\r\n')
    print("shorthand('\\x0a\\x0d')")
    shorthand('\x0a\x0d')
    print("bits('A\\r\\n')")
    bits('A\r\n')
    print("bits('\\x0a\\x0d')")
    bits('\x0a\x0d')


if __name__ == "__main__":
    _tests()

pass # Breakpoint for debugging
