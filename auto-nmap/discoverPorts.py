import argparse
import netifaces
import nmap


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("ip", metavar="IP_ADRESS",
                        nargs=1, help="IP Address of target.")
    parser.add_argument("ps", metavar="PORTS",
                        nargs=1, help="Target ports.")
    args = parser.parse_args()

    return args


def nmap_port_scan(ip_address: str, ports: int) -> None:
    """Ascertain IP address & port types/number and port scan of host(s)"""
    nma = nmap.PortScanner()
    nma.scan(ip_address, ports)
    print("Retrieving data...")
    print(nma.csv())


def main():
    args = parse_cmdline()
    ip_address = args.ip[0]
    ports = args.ps[0]
    print(f"printing cmd line'd ip: {ip_address}, {ports}")
    nmap_port_scan(ip_address=ip_address, ports=ports)
    print("Done!")
    

if __name__ == "__main__":
    main()