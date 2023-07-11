#include <stdio.h>  
#include <stdlib.h>  
#include <errno.h>  
#include <string.h>
#include <winSock2.h>
#include <windows.h>
#include <sys/types.h>  
#pragma comment(lib,"Ws2.lib") //(lib,"Ws2_32.lib")
int OpenTcp(int nMode,char *sParas)  //char *sDevInfo,int iComID,int iBaudrate
{
	WORD wVerisonRequested;
	WSADATA wsaData;
	SOCKET sockClient;
	unsigned char m_strIP[14];
	unsigned char m_strPort[4];
	int err;
	int length=0;
	if (nMode != 1)
	{
		return -1000;
	}
	length = strlen(sParas);
	for (int i = 0; i < length-5; i++)
	{
		m_strIP[i]=sParas[i];
	}

	wVerisonRequested = MAKEWORD(1,1);
	err = WSAStartup(wVerisonRequested, &wsaData);
	if (err != 0)
	{
		printf("连接失败");
		return err;
	}
	// create socket
	sockClient = socket(AF_INET, SOCK_STREAM, 0);
	
	
	// connect server socket
	struct sockaddr_in addrServer;
	addrServer.sin_addr.S_un.S_addr = inet_addr(m_strIP);
	addrServer.sin_family = AF_INET;
	addrServer.sin_port = htons(8000);//atoi(m_strPort)
	int ret = connect(sockClient, (struct sockaddr *)&addrServer, sizeof(addrServer));
	if (ret != 0)
	{
		printf("连接失败！");
		closesocket(sockClient);
		return -1002;
	}
	return sockClient;
}
int main()
{
	SOCKET handle;
	handle = OpenTcp(1,"192.168.1.100,8000");
	printf("OpenTcp = [%d]\n",handle);
	system("pause");
    return 0;
}
