def int(bytes):
    decoded = bytes.decode('ASCII')

    print(decoded)

b = b'\x32'
int(b);
