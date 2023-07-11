#define WIN32_LEAN_AND_MEAN
#include <iostream>
#include <thread>
#include <vector>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")
using namespace std;

int main()
{
	// 启动Windows socket2 环境
	//初始化套节字
	WORD ver = MAKEWORD(2, 2);
	WSADATA dat;
	WSAStartup(ver, &dat);

	// 校验版本
	if (2 != HIBYTE(dat.wVersion) || 2 != LOBYTE(dat.wVersion))
	{
		// 版本不对
		WSACleanup();
		return 0;
	}

	//1 建立一个socket
	SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	sockaddr_in sin = {};
	sin.sin_family = AF_INET;
	sin.sin_port = htons(4567);
	sin.sin_addr.S_un.S_addr = inet_addr("192.168.1.4");
	
	//2 bind 绑定用于接受客户端链接的网络端口
	if (SOCKET_ERROR == bind(sock, (sockaddr*)&sin, sizeof(sin)))
	{
		cout << "绑定网络端口失败" << endl;
	}
	else {
		cout << "绑定网络端口成功" << endl;
	}
	//3. listen监听网络端口
	if (SOCKET_ERROR == listen(sock, 5))
	{
		cout << "监听网络端口失败" << endl;
	}
	else {
		cout << "监听网络端口成功" << endl;
	}

	//4 accept 等待客户端链接
	sockaddr_in clientAddr = {};
	int nAddrLen = sizeof(sockaddr_in);
	SOCKET cSock = INVALID_SOCKET;
	string msg = "Hello, I'm Server";
	cSock = accept(sock, (sockaddr*)&clientAddr, &nAddrLen);
	if (INVALID_SOCKET == cSock)
	{
		cout << "错误,接受到无效客户端SOCKET..." << endl;
	}
	cout << "新客户端加入：" << inet_ntoa(clientAddr.sin_addr) << endl;
	//5 send 向客户端发送数据
	char recvBuf[128] = {};
	while (true)
	{
		int nlen = recv(cSock, recvBuf, 128, 0);
		if (nlen <= 0)
		{
			cout << "客户端退出..." << endl;
			break;
		}
		send(cSock, msg.c_str(), msg.length(), 0);
	}
	

	//6 关闭套接字closesocket
	closesocket(sock);
	//清楚Windows socket环境
	WSACleanup();
}

