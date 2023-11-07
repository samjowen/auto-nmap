<h1> auto_nmap</h1>

A Python-based tool that brings an intuitive approach to network device and port discovery.

<h2> Installation </h2>

Our tool employs Poetry, a powerful Python dependency management system that facilitates smooth installation and package management.

    Use `poetry install` to set up a Python environment that stays automatically up-to-date with the packages that auto_nmap needs.

<h2> Running Tests </h2>

For ensuring your tool's optimal performance, we recommend running the provided tests with the command:

<code> poetry run pytest </code>

This command will initiate the tests located in the /tests/ directory.
<h2> Commands and Their Magic </h2>
<h3> discoverDevices </h3>

Discover every device on your network in a snap with the discoverDevices command.
<li><code> poetry run discoverDevices </code> - Prints out the discovered devices and their respective IPs on your command line.</li>
<li><code> poetry run discoverDevices --output device-ips-on-my-wifi.txt </code> - Saves the IPs of all discovered devices into a file.</li>
<h3> discoverPorts </h3>

Leverage the discoverPorts command to scan and identify open ports on your network devices.
<li><code> poetry run discoverPorts .../txt-files/device-ips-on-my-wifi.txt --ports 22 </code> - Scans a specified port across a list of IPs.</li>
<li><code> poetry run discoverPorts --i 192.168.1.1 --ports 22-999 </code> - Scans a range of ports for a specific IP.</li>
<li><code> poetry run discoverPorts --list .../txt-files/lieksa.txt --ports 1-888 --output lieksa </code> - Scans a range of ports across a list of IPs and stores the results into a file.</li>
<h2> Code Overview </h2>

Our Python script employs classes and methods to perform network scanning tasks effectively.

The Scan class is the heart of our program, encapsulating several methods that perform network scanning.

The methods in the Scan class include:

    get_default_gateway_ip_address: Returns the default gateway IP address of your machine.
    ip_address_to_ip_address_range: Converts an IP address to an IP address range.
    nmap_ping_scan: Executes an nmap ping scan on a given IP or IP range, returning the found hosts.
    write_ip_addresss_to_file: Stores the found hosts into a specified file.
    nmap_port_scan_multihost: Conducts an nmap port scan on multiple hosts and records the results into a specified file.
