import nmap
import netifaces


def get_default_gateway_ip() -> str:
    """ Get the router ip which should be the default gateway"""
    default_gateway_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
    return default_gateway_ip


def ip_to_ip_range(ip: str) -> str:
    """Remove the last 2 or 3 digits from the string after the last ."""
    ip_range = ip.split('.')
    ip_range[-1] = '0-255'
    ip_range = '.'.join(ip_range)
    return ip_range


def nmap_ping_scan(ip: str) -> None:
    """Performs an nmap ping scan on the ip range."""
    nma = nmap.PortScanner()
    nma.scan(hosts=ip, arguments='-sn')
    found_hosts = nma.all_hosts()
    print("Printing hosts...")
    print(found_hosts)
    print(f"Found {len(found_hosts)} hosts!")


def main():
    default_gateway_ip = get_default_gateway_ip()
    ip_range = ip_to_ip_range(default_gateway_ip)
    nmap_ping_scan(ip_range)
    print("Done!")


if __name__ == "__main__":
    main()
