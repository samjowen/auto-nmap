import nmap
import netifaces
import pandas as pd
from io import StringIO

"""
Each host will be in the form of [{'host': ['port': 'state']}????]
"""


class Scan():
    def __init__(self):
        self.target_ip = []
        self.ports = []
        self.location = []
        self.nma = nmap.PortScanner()
        self.hosts = []
        self.results = []

    def get_default_gateway_ip(self) -> str:
        """Catch key error exception if the default gateway cannot be found"""
        try:
            default_gateway_ip = netifaces.gateways(
            )['default'][netifaces.AF_INET][0]
            return default_gateway_ip
        except KeyError:
            raise Exception(
                print("\nOh no, an error!\n\nCould not find default gateway. Are you connected to the internet?\n"))

    def ip_to_ip_range(self, ip: str) -> str:
        """Remove the last 2 or 3 digits from the string after the last ."""
        ip_range = ip.split('.')
        ip_range[-1] = '0-255'
        ip_range = '.'.join(ip_range)
        return ip_range

    def nmap_ping_scan(self, ip: str) -> list[str]:
        """Performs an nmap ping scan on the IP or IP range."""
        nma = self.nma
        nma.scan(hosts=ip, arguments='-sn')
        found_hosts = nma.all_hosts()
        print("Printing hosts...")
        print(found_hosts)
        print(f"Found {len(found_hosts)} hosts!")
        return found_hosts

    def write_ips_to_file(self, found_hosts: list[str], filepath: str) -> None:
        """Write the found hosts to a file separated by newlines."""
        with open(f"{filepath}", 'w+') as f:
            for host in found_hosts:
                f.write(host + '\n')

    def nmap_port_scan_multihost(self, ip_address: list[str], ports: str, filepath: str) -> None:
        """CSV Manipulation here."""
        nma = self.nma
        list_of_dfs = []

        for i in ip_address:
            print(f"Scanning ip_address: {i} for port(s): {ports}.")
            nma.scan(hosts=i, ports=ports)
            csvStringIO = StringIO(nma.csv())
            df = pd.read_csv(csvStringIO, sep=";", header=0)
            list_of_dfs.append(df)

        new_df = pd.concat(list_of_dfs, ignore_index=True)
        with open(f"{filepath}", "w", newline='\n') as myfile:
            new_df.to_csv(myfile, sep=",", index=False)
        self.results = new_df


