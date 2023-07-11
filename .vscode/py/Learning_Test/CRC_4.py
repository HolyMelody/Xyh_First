def crc4(data: str, poly: str = "10011") -> str:
    data = data.ljust(len(data) + len(poly) - 1, "0")
    poly = int(poly, 2)

    data_int = int(data, 2)
    while len(bin(data_int)) >= len(bin(poly)):
        shift = len(bin(data_int)) - len(bin(poly))
        data_int ^= poly << shift

    return bin(data_int)[2:].zfill(4)

data=input("your data: ")##10110011
crc_check = crc4(data)
print("给定数据：", data)
print("CRC-4校验码:", crc_check)
