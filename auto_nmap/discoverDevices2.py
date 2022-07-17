from auto_nmap.Scan import Scan
import argparse
import sys

def parse_cmdline():
    """CLI tool to add parameters to the script."""
    parser = argparse.ArgumentParser(description='discoverPorts of a device.')
    parser.add_argument("--output", metavar="FILEPATH",
                        nargs=1, help="Filepath to .txt file of IP addresses to scan.", required=False)
    args = parser.parse_args()
    return args

def main():
    args = parse_cmdline()
    if not len(sys.argv) > 1:
        scan = Scan()
        router_ip = scan.get_default_gateway_ip()
        scan.target_ip = scan.ip_to_ip_range(router_ip)
        scan.nmap_ping_scan(ip=scan.target_ip)

"""
Todo: Implement the output to a file funtionality.
"""



if __name__ == '__main__':
    main()