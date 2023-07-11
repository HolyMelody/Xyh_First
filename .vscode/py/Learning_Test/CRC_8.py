def crc4(data: str, poly: str = "10011") -> str:
    data = data.ljust(len(data) + len(poly) - 1, "0")
    poly = int(poly, 2)

    data_int = int(data, 2)
    while len(bin(data_int)) >= len(bin(poly)):
        shift = len(bin(data_int)) - len(bin(poly))
        data_int ^= poly << shift

    return bin(data_int)[2:].zfill(4)


def crc8(data: str, poly: str = "100000111") -> str:
    data = data.ljust(len(data) + len(poly) - 1, "0")
    poly = int(poly, 2)

    data_int = int(data, 2)
    while len(bin(data_int)) >= len(bin(poly)):
        shift = len(bin(data_int)) - len(bin(poly))
        data_int ^= poly << shift

    return bin(data_int)[2:].zfill(8)


data=input("Input your data: ")
crc_check = crc8(data)
print("CRC-8校验码:", crc_check)
crc_check = crc4(data)
print("CRC-4校验码:", crc_check)