from io import StringIO

import argparse
import os
import nmap
import pandas as pd


TXT_OUTPUT_FILEPATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'txt-files/'))
CSV_OUTPUT_FILEPATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'csv-files/'))


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')

    parser.add_argument("--ip", metavar="IP_ADDRESS",
                        nargs=1, help="IP Address of target.",
                        required=False, default=None, type=str)

    parser.add_argument("--ports", metavar="PORTS",
                        nargs=1, help="Target ports.",
                        required=True, default=None, type=str)

    parser.add_argument("--list", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt file of IP addresses to scan.",
                        required=False, default=None, type=str)

    parser.add_argument("--output", metavar="OUTPUT_FILEPATH",
                        nargs=1, help="Filepath to .csv file output of the scan.",
                        required=False, default=None, type=str)

    args = parser.parse_args()

    return args


def convert_list_of_ips_to_smallest_and_largest(ip_addresses: list[str]) -> str:
    """Convert a list of IP addresses to the smallest and largest IP address."""
    smallest_ip = ip_addresses[0]
    largest_ip = ip_addresses[-1]
    smallest_ip_host = smallest_ip.split('.')
    largest_ip_host = largest_ip.split('.')
    small_host = smallest_ip_host[-1]
    large_host = largest_ip_host[-1]
    small_host = small_host.strip()
    large_host = large_host.strip()
    ip_str = smallest_ip.split('.')
    ip_str[-1] = small_host + '-' + large_host
    ip_str = '.'.join(ip_str)

    return ip_str


def nmap_port_scan(ip_address: str, ports: str) -> None:
    """Ascertain open port(s) for a single host."""
    nma = nmap.PortScanner()
    nma.scan(hosts=ip_address, ports=ports)
    print(f"Scanning ip_address: {ip_address} for port(s): {ports}.")
    print(nma.csv())


def nmap_port_scan_multihost_legacy(ip_address: str, ports: str) -> None:
    """Ascertain open port(s) for many hosts from a line separated text file."""
    nma = nmap.PortScanner()
    print(f"Scanning ip_addresses: {ip_address} for port(s): {ports}.")
    nma.scan(hosts=ip_address, ports=ports)
    print(nma.csv())


def nmap_port_scan_multihost(ip_address: list[str], ports: str, output: str) -> None:
    """CSV Manipulation here."""
    nma = nmap.PortScanner()
    list_of_data_frames = []

    for i in ip_address:
        print(f"Scanning ip_address: {i} for port(s): {ports}.")
        nma.scan(hosts=i, ports=ports)
        csv_string_io = StringIO(nma.csv())
        data_frame = pd.read_csv(csv_string_io, sep=";", header=0)
        list_of_data_frames.append(data_frame)

    new_data_frame = pd.concat(list_of_data_frames, ignore_index=True)
    with open(f"{CSV_OUTPUT_FILEPATH}/{output}.csv", "w", newline='\n', encoding="UTF8") as myfile:
        new_data_frame.to_csv(myfile, sep=",", index=False)


def main():
    """Main function to run the script."""
    # Initialising the list of ip_addresses so we can use it later in the script.
    ip_addresses = []
    args = parse_cmdline()
    # The ports to scan for. Ports is a required argument for now, so it can live here.
    ports = args.ports[0]

    if args.ip:  # If the user specified an IP address, scan that single IP.
        ip_address = args.ip[0]
        nmap_port_scan(ip_address=ip_address, ports=ports)
        print("Done!")

    if args.list:  # If a list of IP addresses is provided, scan each one.
        filepath = args.list[0]
        with open(filepath, encoding="UTF8") as file:
            for line in file:
                ip_addresses.append(line)
        nmap_port_scan_multihost(
            ip_address=ip_addresses, ports=ports, output=args.output[0])
        print("Done!")


if __name__ == "__main__":
    main()
