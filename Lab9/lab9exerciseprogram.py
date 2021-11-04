def main():
    c = 41476
    n = 60491
    z = 60000
    d = findD(z)
    m = findM(c, d, n)
    print("c = " + str(c))
    print("d = " + str(d))
    print("m = " + str(m))
    print("n = " + str(n))
    print("z = " + str(z))



def findD(z):
    for i in range(z):
        value = 17 * i
        if value % z == 1:
            print(i)
            return i


def findM(c, d, n):
    return pow(c, d, n)

main()
