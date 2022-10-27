import socket
import threading
from config import *
import datetime
import time

SIZE = 1024
PORT   = 5050
IP = socket.gethostbyname(socket.gethostname()) 
ADDR = (IP , PORT) 
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(ADDR) 

files_content_table = {} # this is a dict which contains "path" : [files content in list]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        if msg := conn.recv(SIZE).decode(FORMAT).rstrip('\x00'): # if the message have some content
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")
            start_time = time.time()
            
            ## TODO : split msg into 
            ## "string" and "path"

            if REREAD_ON_QUERY : 
                output = search_string_reload(TXT_FILES_PATHS[0] , msg)            
            else:
                output = search_string(TXT_FILES_PATHS[0] , msg)
            total_time = time.time() - start_time
            ######################
            ## TODO : put this in a log file 
            print(f"[DEBUG] ::{datetime.datetime.now()}:: ::{msg}:: ::{output}:: ::{total_time} s:: ")
            #######################      
            conn.sendall(f"{output}".encode(FORMAT))

    conn.close()



def main():
    server.listen() # Makes the server "Listenting"
    print(f"[LISTENTING] Server is listening on {IP}")
    while True :
        conn , addr = server.accept() # Blocking part to wait for connection
        thread = threading.Thread(target=handle_client , args=(conn , addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


def read_files():
    """ This function reads all .txt files to be save to a dict of lists"""
    print("[READING] Reading all the text files in the server. ")
    for path in TXT_FILES_PATHS:
        files_content_table[path] = []
        # Read all the text in the files 
        with open(path) as file:
            for line in file:
                files_content_table[path].append(line.strip().rstrip('\x00'))

def search_string(file_path , q_string):
    """
    This function searchs for a string in an exact .txt file path 
    witout rereading the file
    ::file_path:: the .txt file 
    ::q_string:: the string to search for 
    """
    return "STRING EXISTS\n" if q_string in files_content_table[file_path] else "STRING NOT FOUND\n"


def search_string_reload(file_path , q_string):
    """
    This functions searchs for the string in an exact .txt file path with rereading the file
    ::file_path:: .txt file path
    ::q_string:: the string to search for 
    """
    try : 
        with open(file_path) as file:
           return next(("STRING EXISTS\n" for line in file if line.strip().rstrip('\x00') == q_string), "STRING NOT FOUND\n")           
    except Exception as e: 
        print(f"[ERROR] Error in the path name : {e}.")
        return "STRING NOT FOUND\n"

if __name__ == '__main__':
    print("[STARTING] server is starting...")
    read_files()
    main()






