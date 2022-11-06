import socket
import threading
import datetime
import time
from configparser import ConfigParser
import subprocess

config = ConfigParser() # Initiating the configuration parser 
config.read("configuration.ini") # Getting the desired configuration file

REREAD_ON_QUERY = True # Flag for reloading or nor 
SIZE = 1024  # Size of the message
PORT   = 5557 # Port used  
IP = '' # Ip to be connected to the client .. it is blank as the private is the public (no port fowarding)
ADDR = (IP , PORT) # Comibining the IP and Port 
FORMAT = "utf-8" # Encoding and deconding format 

# Socket Initialization 
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # Initiating TCP socket 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reusing the port address 
server.bind(ADDR) # Bindin the server with the address and the port 

FILES_CONTENT_TABLE = {} # Table to store the file's content for faster retrieval as DB

def handle_client(conn, addr):
    """ Handling client connection
    
    :conn: Connection object
    :addr: Address of the client 
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # Waiting for a message from the client to process some logic 
        if msg := conn.recv(SIZE).decode(FORMAT).rstrip('\x00'):
                        
            print(f"[{addr}] {msg}") # Printing , just for logginf 
            
            start_time = time.time() # start calculating time 
            msg = check_msg(msg) # Getting the text out of the message 
            if msg is None: # If there is no text then continue looping till somethng useful comes
                continue

            # Getting the result of the message 
            output = search_string_reload(msg) if REREAD_ON_QUERY else search_string(msg)

            total_time = time.time() - start_time # Calculates the total time of the searching process 
            print(f"[DEBUG] ::{datetime.datetime.now()}:: ::{msg}:: ::{output}:: ::{total_time} s:: ")
            conn.sendall(f"{output}".encode(FORMAT)) # Sends back to the client the result  
        
        else:
            connected = False

    conn.close() # Close the connection once the loop broke 


def main():
    """ Main function to handle the connections in threads """
    server.listen(4096) # Makes the server "Listenting" , backlog = 4096 check /proc/sys/net/core/somaxconn
    print(f"[LISTENTING] Server is listening on {IP}")
    while True : # Always listen for new connections 
        conn , addr = server.accept() # Blocking part to wait for connection
        thread = threading.Thread(target=handle_client , args=(conn , addr)) # New thread to handle the new connection 
        thread.start() # Start the thread
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


def read_files():
    """ This function reads all .txt files to be save to a dict of lists"""
    print("[READING] Reading all the text files in the server. ")
    try :
        global FILES_CONTENT_TABLE # Use the global variable to store the content of the text file 
        with open(config["PATH"]["linuxpath"]) as file:  # Open the file and loop through each line 
            for line in file:
                FILES_CONTENT_TABLE[line.strip().rstrip('\x00')] = True # Make a dict of {'line' : True} contains all lines
    except KeyError:
        print("FILE IS NOT FOUND !\n")

def search_string(q_string):
    """
    Returns STRING EXISTS or STRING NOT FOUND string,
    this works when REREAD_ON_QUERY is Flase 
    
    :q_string: the string to search for 
    """
    try :
        if FILES_CONTENT_TABLE[q_string] : # check in the global dict.
            return "STRING EXISTS\n"
    except KeyError:
        return "STRING NOT FOUND\n"



def search_string_reload(q_string):
    """
    Returns STRING EXISTS or STRING NOT FOUND string,
    this works when REREAD_ON_QUERY is True 

    :q_string: the string to search for 
    """
    try: # Handling of the searching in the path 

        # Subprocess runs linux comand for fast retrieval for the information , returns int 
        # Calling "Grep" command 
        # 0 ==> string found in the file
        # other than 0 ==> string not found in the file  
        if subprocess.call(['/bin/grep', q_string, config["PATH"]["linuxpath"]]) == 0 : 
            return "STRING EXISTS\n"  
        else : 
            return 'STRING NOT FOUND\n'
    except Exception as e :
        return f'PROBLEM IN SEARCHING IN TEXT FILE {e}\n'                


def check_msg(msg):
    """ Returns the "string" of the message recieved 
        Or None 

        :msg: msg came from the client 
    """
    msg = msg.strip() # Strip the message from any spaces 
    return None if msg == '' else msg # If empty then return None else return the message 

if __name__ == '__main__': # When the server .py file runs 
    read_files() # Read the file to retrieve fast from the beggining when flag is false
    main() 

