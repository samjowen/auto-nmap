import argparse
import sys
from auto_nmap.Scan import Scan


def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("--output", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt of IP addresses to scan.", required=False)
    args = parser.parse_args()
    return args


def main():
    """Main function to run the script."""
    if len(sys.argv) <= 1:
        scan = Scan()
        router_ip = scan.get_default_gateway_ip()
        scan.target_ip = scan.ip_to_ip_range(router_ip)
        scan.nmap_ping_scan(ip=scan.target_ip)


if __name__ == '__main__':
    main()
