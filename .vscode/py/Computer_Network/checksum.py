def checksum(str):
	csum = 0  # 校验和  （一个32位十进制数，因为每16位相加时可能会产生进位（即溢出），这些溢出将会被回卷）
	# 奇偶控制，如果总长的字节数为奇数时，肯定最后一个字节要单独相加（求校验和时是每16位一加）
	countTo = (len(str) // 2) * 2
	count = 0
	while count < countTo:
		# ord()函数返回一个字符的ASCII码
		# 取两个字节，第二个字节放在16位的高位，第一个字节放在16位的地位
		thisVal = (str[count + 1] << 8) + str[count]
		csum = csum + thisVal
		# 这里和0xffffffff进行and运算主要是为了保留每次运算过程中可能出现的16位溢出，
		# 这样一来，就可以将溢出位（也就是进位）保存到sum的高16位
		csum = csum & 0xffffffff
		count = count + 2  # 后移两个字节，也就是准备求和下一个16位

	# 如果真的有一个字节剩余
	if countTo < len(str):
		csum = csum + str[len(str) - 1].decode()
		csum = csum & 0xffffffff

	# 把csum的高16位溢出回卷，加到低16位上
	csum = (csum >> 16) + (csum & 0xffff)
	# 如果还产生了溢出，再操作一次
	csum = csum + (csum >> 16)
	# 求反码
	answer = ~csum
	answer = answer & 0xffff
	# 这里进行字节序大小端转换，因为网络字节序是大端模式
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

