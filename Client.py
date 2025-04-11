import socket
import struct

from tkinter import filedialog,Tk

from InquirerPy import inquirer
from InquirerPy.base import Choice



def reciever(client_socket):
    file_size_raw=client_socket.recv(8)
    file_size=struct.unpack('!Q',file_size_raw)[0]

    content=client_socket.recv(file_size)
    return content

def save_file(extension):
    root=Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.asksaveasfilename(defaultextension=extension, filetypes=[(f"{(extension.lstrip('.')).upper()} files", f"*{extension}"),("Text files", "*.txt"), ("All files", "*.*")])
    root.destroy()
    return file_path


def recv_file(client_socket,chunk_size,extension):
    file_size_raw=client_socket.recv(8)
    file_size=struct.unpack('!Q',file_size_raw)[0]
    
    file_path=save_file(extension)
    if file_path:
        try:
            with open(file_path, 'wb') as file:
                received=0
                while received<file_size:
                    content=client_socket.recv(min(chunk_size,file_size-received))
                    file.write(content)
                    received+=len(content)
        except Exception as e:
            print(f"Error saving file: {str(e)}")

def start():
    client_socket = socket.socket()
    addr = '127.0.0.1'
    port = 8080
    try:
        client_socket.connect((addr, port))
        print("Socket connection successful")
    except:
        print("Socket Connection failed")
    c = inquirer.select(message=f"Do you agree to receive the file '{reciever(client_socket).decode()}'?",
                        choices=["Yes", "No", Choice(value=None, name="Exit")],
                        default=None).execute()

    chunk_size = 4096

    if c == "Yes":
       extension=reciever(client_socket).decode()
       recv_file(client_socket,chunk_size,extension)
    if c == "No":
        print("Transfer declined.")
    if c is None:
        exit(1)







