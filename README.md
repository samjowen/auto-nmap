<h1> auto_nmap </h1>
<h2> Installation </h2>
This project was built with the Poetry dependency manager.

1. Use <code>poetry install</code> to create a new python environment/interpreter that will stay up to date with the packages that are needed to run these scripts.

<hr>

<br>
<h2> Running Tests </h2>

Use the command:
<br>
<code> poetry run pytest </code> to run the tests found in the /tests/ directory.
<br>

<hr>
<br>
<h2> Example Commands </h2>
<h3> discoverDevices </h3>
<li><code> poetry run discoverDevices </code> (cmd line print out of devices found IPs)</li>
<li><code> poetry run discoverDevices --output device-ips-on-my-wifi.txt </code> (outputs devices found IPs to a file)</li>
<br>
<br>
<h3> discoverPorts </h3>
<li> <code> poetry run discoverPorts .../txt-files/device-ips-on-my-wifi.txt --ports 22 </code> (IP list scanning mode)
<li> <code> poetry run discoverPorts --i 192.168.1.1 --ports 22-999 </code> (single IP scanning mode)
<li> <code> poetry run discoverPorts --list .../txt-files/lieksa.txt --ports 1-888 --output lieksa </code> (IP list  port scanning mode)
