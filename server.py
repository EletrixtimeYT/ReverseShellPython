import socket
import time

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Listening on :  {host}:{port}")

    client_socket, client_address = server_socket.accept()
    client_username = client_socket.recv(1024).decode()

    print(f"Connected to {client_address}. Username {client_username}")
    print("Type !help for get informations")
    while True:

        command = input(f"{client_address}@{client_username} : ")
        if command.lower() == '!exit':
            break
        elif command == command.lower() == "!help":
            print(""""
------HELP------                
!help : show help :)
!exit : exit                 
                  
                  
                  """)
        retries = 10
        while retries > 0:
            client_socket.send(command.encode())
            time.sleep(1)  

            try:
                output = client_socket.recv(1024).decode()
                print(f"{output}")
                break
            except socket.error as e:
                print(f"COM ERR WITH {e}")
                retries -= 1
                print(f"Retries : {retries}")

        if retries == 0:
            print(f"COM ERR WITH {client_username} ")
            with open("impactlog.txt", "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: FAIL RUN '{command}' FOR {client_username}\n")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
