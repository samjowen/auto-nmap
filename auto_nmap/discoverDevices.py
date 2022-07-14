import netifaces
import nmap
import argparse
import os

OUTPUT_FILEPATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'txt-files/'))


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("--output", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt file of IP addresses to scan.", required=False)
    args = parser.parse_args()
    return args


def write_ips_to_file(found_hosts: list[str], filename: str) -> None:
    """Write the found hosts to a file."""
    f = open(OUTPUT_FILEPATH + "/" + filename, 'w+')
    for host in found_hosts:
        f.write(host + '\n')
    f.close()


def get_default_gateway_ip() -> str:
    """ Get the router ip which should be the default gateway"""
    """Catch key error exception if the default gateway cannot be found"""
    try:
        default_gateway_ip = netifaces.gateways(
        )['default'][netifaces.AF_INET][0]
        return default_gateway_ip
    except KeyError:
        raise Exception(
            "Could not find default gateway. Are you connected to the internet?")


def ip_to_ip_range(ip: str) -> str:
    """Remove the last 2 or 3 digits from the string after the last ."""
    ip_range = ip.split('.')
    ip_range[-1] = '0-255'
    ip_range = '.'.join(ip_range)
    return ip_range


def nmap_ping_scan(ip: str) -> list[str]:
    """Performs an nmap ping scan on the IP or IP range."""
    nma = nmap.PortScanner()
    nma.scan(hosts=ip, arguments='-sn')
    found_hosts = nma.all_hosts()
    print("Printing hosts...")
    print(found_hosts)
    print(f"Found {len(found_hosts)} hosts!")
    return found_hosts


def main():
    args = parse_cmdline()
    if args == None:
        """If no arguments are provided, default to printing the hosts to the command line."""
        default_gateway_ip = get_default_gateway_ip()
        ip_range = ip_to_ip_range(default_gateway_ip)
        nmap_ping_scan(ip_range)
        print("Done!")

    elif args.output:
        """If an output filepath is provided, write the hosts to the file."""
        default_gateway_ip = get_default_gateway_ip()
        ip_range = ip_to_ip_range(default_gateway_ip)
        found_hosts = nmap_ping_scan(ip_range)
        write_ips_to_file(found_hosts=found_hosts, filename=args.output[0])
        print("Wrote file to output folder!")


if __name__ == "__main__":
    main()
