import socket
from tkinter import filedialog,Tk
import struct
import os


def open_file():    
    root=Tk()
    root.withdraw()
    root.attributes("-topmost",True)
    filepath=filedialog.askopenfilename()
    root.destroy()
    return filepath

def read(filepath:str)->str:
    with open(filepath, 'rb') as file:
            content = file.read()
            INITIAL_FILE_SIZE=len(content)
            file_name=os.path.basename(filepath)
            extension=os.path.splitext(filepath)[1]

            print(f"/n Size of data {INITIAL_FILE_SIZE} bytes")
            
            return file_name,INITIAL_FILE_SIZE,filepath,extension

def sender(conn,content):
     FILE_SIZE=len(content)
     conn.send(struct.pack('!Q',FILE_SIZE))
     conn.sendall(content)

def send_file(conn,fsize,filepath,chunk_size):
     sent=0

     conn.send(struct.pack('!Q',fsize))

     with open(filepath, 'rb') as file:
          while sent<fsize:
            chunk=file.read(min(chunk_size,fsize-sent))
            conn.sendall(chunk)
            sent+=len(chunk)

def start():
        
    version="1.0.0"

    server_socket=socket.socket()
    addr='127.0.0.1'
    port=8080

    try:
        server_socket.bind((addr,port))
        server_socket.listen(1)

    except:
        print("socketection Failed")
    conn,_=server_socket.accept()
    FILE_NAME,FILE_SIZE,filepath,extension=read(open_file())

    chunk_size = 4096

    sender(conn,FILE_NAME.encode())

    sender(conn,extension.encode())

    send_file(conn,FILE_SIZE,filepath,chunk_size)

    print("Data transmission completed")




     