import argparse
import os
import sys

import netifaces
import nmap

TXT_OUTPUT_FILEPATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'txt-files/'))


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("--output", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt of IP addresses to scan.", required=False)
    args = parser.parse_args()
    return args


def write_ips_to_file(found_hosts: list[str], filename: str) -> None:
    """Write the found hosts to a file."""
    with open(TXT_OUTPUT_FILEPATH + "/" + filename, 'w+', encoding="UTF8") as file:
        for host in found_hosts:
            file.write(host + '\n')


def get_default_gateway_ip() -> str:
    """ Get the router ip which should be the default gateway"""
    try:
        default_gateway_ip = netifaces.gateways(
        )['default'][netifaces.AF_INET][0]
        return default_gateway_ip
    except KeyError as exc:
        raise KeyError("No default gateway found.") from exc


def ip_to_ip_range(ip_address: str) -> str:
    """Remove the last 2 or 3 digits from the string after the last ."""
    ip_range = ip_address.split('.')
    ip_range[-1] = '0-255'
    ip_range = '.'.join(ip_range)
    return ip_range


def nmap_ping_scan(ip_address: str) -> list[str]:
    """Performs an nmap ping scan on the IP or IP range."""
    nma = nmap.PortScanner()
    nma.scan(hosts=ip_address, arguments='-sn')
    found_hosts = nma.all_hosts()
    print("Printing hosts...")
    print(found_hosts)
    print(f"Found {len(found_hosts)} hosts!")
    return found_hosts


def main():
    """Main function to run the script."""
    args = parse_cmdline()
    # If the arguments provided are not greater than 1, i.e., 0, do this default method.
    if len(sys.argv) <= 1:
        print("No arguments given. Defaulting to command line output.")
        print("Finding default gateway IP...")
        default_gateway_ip = get_default_gateway_ip()
        print(f"Default gateway IP: {default_gateway_ip}")
        ip_range = ip_to_ip_range(default_gateway_ip)
        print("Scanning for devices...")
        nmap_ping_scan(ip_range)
        print("Done!")

    elif args.output:  # If the user specified an output file, write the hosts to that file.
        default_gateway_ip = get_default_gateway_ip()
        ip_range = ip_to_ip_range(default_gateway_ip)
        found_hosts = nmap_ping_scan(ip_range)
        write_ips_to_file(found_hosts=found_hosts, filename=args.output[0])
        print("Wrote file to output folder!")


if __name__ == "__main__":
    main()
