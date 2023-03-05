from io import StringIO

import nmap
import netifaces
import pandas as pd


class Scan():
    def __init__(self):
        self.target_ip_address = []
        self.ports = []
        self.location = []
        self.nma = nmap.PortScanner()
        self.hosts = []
        self.results = []

    def get_default_gateway_ip_address(self) -> str:
        """Catch key error exception if the default gateway cannot be found"""
        try:
            default_gateway_ip_address = netifaces.gateways(
            )['default'][netifaces.AF_INET][0]
            return default_gateway_ip_address
        except KeyError as exc:
            raise KeyError("No default gateway found.") from exc

    def ip_address_to_ip_address_range(self, ip_address: str) -> str:
        """Remove the last 2 or 3 digits from the string after the last ."""
        ip_address_range = ip_address.split('.')
        ip_address_range[-1] = '0-255'
        ip_address_range = '.'.join(ip_address_range)
        return ip_address_range

    def nmap_ping_scan(self, ip_address: str) -> list[str]:
        """Performs an nmap ping scan on the ip_address or ip_address range."""
        nma = self.nma
        nma.scan(hosts=ip_address, arguments='-sn')
        found_hosts = nma.all_hosts()
        print("Printing hosts...")
        print(found_hosts)
        print(f"Found {len(found_hosts)} hosts!")
        return found_hosts

    def write_ip_addresss_to_file(self, found_hosts: list[str], filepath: str) -> None:
        """Write the found hosts to a file separated by newlines."""
        with open(f"{filepath}", 'w+', encoding="UTF8") as file:
            for host in found_hosts:
                file.write(host + '\n')

    def nmap_port_scan_multihost(self, ip_address: list[str], ports: str, filepath: str) -> None:
        """CSV Manip_addressulation here."""
        nma = self.nma
        list_of_dfs = []

        for i in ip_address:
            print(f"Scanning ip_address: {i} for port(s): {ports}.")
            nma.scan(hosts=i, ports=ports)
            csv_string_io = StringIO(nma.csv())
            data_frame = pd.read_csv(csv_string_io, sep=";", header=0)
            list_of_dfs.append(data_frame)

        new_df = pd.concat(list_of_dfs, ignore_index=True)
        with open(f"{filepath}", "w", newline='\n', encoding="UTF8") as myfile:
            new_df.to_csv(myfile, sep=",", index=False)
        self.results = new_df
