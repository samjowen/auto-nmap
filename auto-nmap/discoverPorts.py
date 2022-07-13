import argparse
import netifaces
import nmap

from discoverDevices import *

def nmap_port_scan():    
    """Ascertain IP address & port types/number and port scan of host(s)"""
    nma = nmap.PortScanner()
    ip_address = input('Please input an IP address for scanning: ')
    ports = input('Please input the ports you are scanning; i.e., 1, 1-1000, 5-25: ')
    nma.scan(ip_address, ports)
    print(nma.csv())

def main():
   nmap_port_scan()


if __name__ == "__main__":
    main()