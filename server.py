from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, timeout
import sys
import time



UDPPORT = int(sys.argv[1])
TCPPORT = UDPPORT+1

BUFFER_SIZE = int(sys.argv[2])
TEST_TIME = 20

TEST1 = 'TEST1'.encode()
TEST2 = 'TEST2'.encode()
TEST3 = 'TEST3'.encode()
TEST4 = 'TEST4'.encode()

host='0.0.0.0'
msg = bytearray(BUFFER_SIZE)
test_package = bytearray(BUFFER_SIZE)



def main():
	udp = socket(AF_INET, SOCK_DGRAM)
	tcp = socket(AF_INET, SOCK_STREAM)

	tcp.bind((host, TCPPORT))
	udp.bind((host, UDPPORT))

	tcp.listen(2)
	con, addr = tcp.accept()
	conn_check, addr_check = tcp.accept() 

	print('Conexões aceitas')


	print("TCP TEST")
	tcp_download_test(con, conn_check)
	tcp_upload_test(con, conn_check)

	print("\nUDP TEST")
	udp_client = udp_download_test(udp, conn_check)
	udp_upload_test(udp, conn_check, udp_client)



	tcp.close()
	udp.close()

def tcp_download_test(con, conn_check):
	total_bytes = 0
	pacotes = 0

	while True:
		check_msg = conn_check.recv(BUFFER_SIZE).strip()
		if check_msg == TEST1:
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


def tcp_upload_test(con, conn_check):
	start = time.time()
	end = time.time()
	total_bytes = 0
	pacotes = 0

	conn_check.send(TEST2)
	
	while(end - start < TEST_TIME):
		total_bytes += con.send(test_package)
		pacotes += 1
		end = time.time()

	print(f'Upload> Velocidade: {pacotes*8/(TEST_TIME):.2f} Mb/s	Pacotes/s: {pacotes/TEST_TIME} 	 Bytes Transferidos: {total_bytes}    Tempo: {TEST_TIME}')



def udp_download_test(udp, conn_check):
	total_bytes = 0
	pacotes = 0

	while True:
		check_msg = conn_check.recv(BUFFER_SIZE).strip()
		if check_msg == TEST3:
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

	return udp_client



def udp_upload_test(udp, conn_check, udp_client):
	start = time.time()
	end = time.time()
	total_bytes = 0
	pacotes = 0
	
	conn_check.send(TEST4)
	
	while(end - start < TEST_TIME):
		total_bytes += udp.sendto(test_package, udp_client)
		pacotes += 1
		end = time.time()

	conn_check.send(pacotes.to_bytes(4, byteorder="big"))
	print(f'Upload> Velocidade: {pacotes*8/(TEST_TIME):.2f} Mb/s	Pacotes/s: {pacotes/TEST_TIME} 	 Bytes Transferidos: {total_bytes}    Tempo: {TEST_TIME}')



if __name__ == "__main__":
    main()
	