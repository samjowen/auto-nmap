import argparse

import nmap

"""
Sample command:
python discoverPorts.py .../Users/samjowen/Desktop/auto-nmap/auto-nmap/auto-nmap/txt-files/ips.txt --ports 22
"""


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("--ip", metavar="IP_ADDRESS",
                        nargs=1, help="IP Address of target.", required=False)
    parser.add_argument("--ports", metavar="PORTS",
                        nargs=1, help="Target ports.", required=True)
    parser.add_argument("--list", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt file of IP addresses to scan.", required=False)
    args = parser.parse_args()

    return args


def nmap_port_scan(ip_address: str, ports: int) -> None:
    """Ascertain open port(s) for a single host."""
    nma = nmap.PortScanner()
    nma.scan(hosts=ip_address, ports=ports)
    print("Retrieving data...")
    print(nma.csv())


def nmap_port_scan_multihost(ip_address: str, ports: int) -> None:
    """Ascertain open port(s) for many hosts from a line separated text file."""
    nma = nmap.PortScanner()
    for i in ip_address:
        print(
            f"Scanning host {i} for port(s) {ports} ({ip_address.index(i) + 1} of {len(ip_address)} hosts).")
        nma.scan(hosts=i, ports=ports)
        print(nma.csv())


def main():
    # Initialising the list of ip_addresses so we can use it later in the script.
    ip_addresses = []
    args = parse_cmdline()
    # The ports to scan for. Ports is a required argument for now, so it can live here.
    ports = args.ports[0]

    if args.ip:  # If the user specified an IP address, scan that single IP.
        ip_address = args.ip[0]
        nmap_port_scan(ip_address=ip_address, ports=ports)
        print("Done!")

    elif args.list:  # If a list of IP addresses is provided, scan each one.
        filepath = args.list[0]
        with open(filepath) as f:
            for line in f:
                ip_addresses.append(line)
        nmap_port_scan_multihost(ip_address=ip_addresses, ports=ports)
        print("Done!")


if __name__ == "__main__":
    main()
