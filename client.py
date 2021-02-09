from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, timeout
import sys
import time

HOST = sys.argv[1]
UDPPORT = int(sys.argv[2])
TCPPORT = UDPPORT+1

UDPDEST = (HOST, UDPPORT) 
TCPDEST = (HOST, TCPPORT)

BUFFER_SIZE = int(sys.argv[3])
TEST_TIME = 20

TEST1 = 'TEST1'.encode()
TEST2 = 'TEST2'.encode()
TEST3 = 'TEST3'.encode()
TEST4 = 'TEST4'.encode()

msg = bytearray(BUFFER_SIZE)
test_package = bytearray(BUFFER_SIZE)


def main():
    udp = socket(AF_INET, SOCK_DGRAM)
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp_check = socket(AF_INET, SOCK_STREAM)


    tcp.connect(TCPDEST)
    tcp_check.connect(TCPDEST)

    print('Ambos sockets conectados')

    print('TCP TEST:')
    tcp_upload(tcp, tcp_check)
    tcp_download(tcp, tcp_check)

    print('UDP TEST:')
    udp_upload(udp, tcp_check)
    udp_download(udp, tcp_check)

    udp.close()
    tcp.close()
    tcp_check.close()



def tcp_upload(con, conn_check):
	start = time.time()
	end = time.time()
	total_bytes = 0
	pacotes = 0

	conn_check.send(TEST1)
	
	while(end - start < TEST_TIME):
		total_bytes += con.send(test_package)
		pacotes += 1
		end = time.time()

	print(f'Upload> Velocidade: {pacotes*8/(TEST_TIME):.2f} Mb/s	Pacotes/s: {pacotes/TEST_TIME} 	 Bytes Transferidos: {total_bytes}    Tempo: {TEST_TIME}')



def tcp_download(con, conn_check):
	total_bytes = 0
	pacotes = 0

	while True:
		check_msg = conn_check.recv(BUFFER_SIZE).strip()
		if check_msg == TEST2:
			break

	try:
		while True:
			con.settimeout(1)
			recv_bytes = con.recv_into(msg, BUFFER_SIZE)
			pacotes+=1
			total_bytes += recv_bytes
		
	except: timeout
	con.settimeout(None)

	print(f'Download> Velocidade: {total_bytes*8/1024/(TEST_TIME-1):.2f} Mb/s	Pacotes/s:{pacotes/TEST_TIME}	Bytes Transferidos: {total_bytes}	Tempo: {TEST_TIME}')



def udp_upload(udp, conn_check):
	start = time.time()
	end = time.time()
	total_bytes = 0
	pacotes = 0
	
	conn_check.send(TEST3)
	
	while(end - start < TEST_TIME):
		total_bytes += udp.sendto(test_package, UDPDEST)
		pacotes += 1
		end = time.time()

	conn_check.send(pacotes.to_bytes(4, byteorder="big"))
	print(f'Upload> Velocidade: {pacotes*8/(TEST_TIME):.2f} Mb/s	Pacotes/s: {pacotes/TEST_TIME} 	 Bytes Transferidos: {total_bytes}    Tempo: {TEST_TIME}')



def udp_download(udp, conn_check):
	total_bytes = 0
	pacotes = 0

	while True:
		check_msg = conn_check.recv(BUFFER_SIZE).strip()
		if check_msg == TEST4:
			break
		
	try:
		while True:
			udp.settimeout(1)
			recv_bytes, udp_client = udp.recvfrom_into(msg, BUFFER_SIZE)
			pacotes+=1
			total_bytes += recv_bytes

	except: timeout
	udp.settimeout(None)

	total_pkgs = conn_check.recv(BUFFER_SIZE);

	print(f'TOTAL: {int.from_bytes(total_pkgs, byteorder = "big")}')
	print(f'Download> Velocidade: {total_bytes*8/1024/(TEST_TIME):.2f} Mb/s	Pacotes/s:{pacotes/TEST_TIME}	Perca de pacotes: {100-pacotes/int.from_bytes(total_pkgs, byteorder="big")*100:.2f}% 	Bytes Transferidos: {total_bytes}	Tempo: {TEST_TIME}')



if __name__ == "__main__":
    main()