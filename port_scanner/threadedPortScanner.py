import threading
import socket
from queue import Queue





global target
target = "IP_address"  #target is the IP-adress of the host we are trying to scan
queue = Queue()
open_ports = [] #open_ports will store all open port numbers

def portscan(port):

    try:
        #Connecting via TCP, if using UDP arg 2 is socket.SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def get_ports(mode):
    if mode == 1:
        #Scans the standardised 1023 ports
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        #Scans the standardised and reserved ports
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        #Scans teh reserved ports for predefined protocols such as SSH
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        #Allows manual choice of the port to scan
        ports = input("Enter your ports (seperate by blank):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)   

def worker():
    #Function is responsible for getting the port numbers from the queue and scanning them
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)
        """
        else:
            print("Port {} is closed!".format(port))
        """

def run_scanner(threads, mode):
    """
    the function gets all the available ports and depending on the number of threads each thread assigned
    to a worker function and adds them to a list, after which they scan all the ports and providing all the open ports
    """
    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)
"""
def scanPorts():
    for port in range(1, 1024):
        result = portscan(port)
        if(result):
            print("Port {} is open!".format(port))
        else:
            print("Port {} is closed!".format(port))
"""     

def main():
    mode = input("Enter your desired mode: ")
    threads = input("Ente your desired amount of threads: ")
    run_scanner(mode, threads)

if __name__ == "__main__":
    main()