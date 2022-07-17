from importlib.resources import path
import os
import netifaces
import mock

import pytest
from auto_nmap import __version__
from auto_nmap.discoverDevices import get_default_gateway_ip, ip_to_ip_range
from auto_nmap.discoverPorts import convert_list_of_ips_to_smallest_and_largest, parse_cmdline
from mock import Mock
from auto_nmap.Scan import Scan

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..',))
OUTPUT_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'auto_nmap/txt-files/'))

mocker = Mock()


def test_version():
    assert __version__ == '0.1.0'


"""Start testing of discoverDevices.py"""


def test_convert_list_of_ips_to_smallest_and_largest(script_runner):
    """Test the convert_list_of_ips_to_smallest_and_largest function. This should return one address range."""
    assert convert_list_of_ips_to_smallest_and_largest(
        ['192.168.0.1', '192.168.0.55']) == '192.168.0.1-55'


def test_ip_to_ip_range():
    """Test the ip_to_ip_range function. This should remove the the host part of the IP address and replace it with 0-255."""
    assert ip_to_ip_range('192.168.0.1') == '192.168.0.0-255'


def test_exception_get_default_gateway_ip(mocker):
    """Test the get_default_gateway_ip function. This should raise an exception if the default gateway cannot be found."""
    with pytest.raises(Exception):
        # Mock the get_default_gateway_ip function to raise an exception by simulating no wifi connection.
        mocker.patch(get_default_gateway_ip(), return_value=KeyError)


def test_help_argparse(script_runner):
    result = script_runner.run('discoverDevices', '-h')
    assert result.success


def test_help_argparse(script_runner):
    result = script_runner.run('discoverDevices', '-h')
    assert result.success


def test_bad_argument_argparse(script_runner):
    result = script_runner.run('discoverDevices', '-badArgument')
    assert result.success == False


# def test_output_ips_to_text_file(script_runner):
#    script_runner.run('discoverDevices', '--output', 'test.txt')
#    """Check if the output file exists."""
#    file = pathlib.Path(OUTPUT_DIR + "/test.txt")
#    assert file.exists()


"""Start testing of Scan.py"""

"""Test class Scan"""


def test_Scan_instantiate():
    """Test the Scan class init function. This should create a Scan object."""
    testScan = Scan()
    assert testScan.__class__.__name__ == 'Scan'


def test_Scan_get_default_gateway_ip():
    """Test the Scan class get_default_gateway_ip function. This should return the default gateway IP."""
    testScan = Scan()
    testScan.target_ip = testScan.get_default_gateway_ip()

    assert testScan.target_ip == netifaces.gateways()[
        'default'][netifaces.AF_INET][0]


def test_Scan_ip():
    """Test the Scan class'function to call a class within another. 
    This should return the CSV output which contains the 'hostname' string."""
    testScan = Scan()
    testScan.target_ip = '192.168.0.1'
    scan = testScan.nma.scan(hosts=testScan.target_ip, arguments='-sP')
    print(scan)
    assert testScan.nma.csv().__contains__('hostname')


def test_nmap_port_scan_multihosts():
    """Test the Scan class'function to call a class within another. 
    This should return the CSV output which contains the 'hostname' string."""
    testScan = Scan()
    testScan.target_ip = '192.168.0.1'
    testScan.nmap_port_scan_multihost(ip_address=[
                                      testScan.target_ip, testScan.get_default_gateway_ip()], ports='22-80', output='meow.csv')
    with open('test.csv', 'r') as f:
        assert f.read().__contains__('hostname')
    # delete test.csv
    os.remove('test.csv')


def test_Scan_ping_sweep_home_network():
    """Test if the new OOP approach work, we should be able to recreate the old main methods of discoverDevices.py."""
    testScan = Scan()
    testScan.target_ip = testScan.ip_to_ip_range(
        testScan.get_default_gateway_ip())
    ip_list = testScan.nmap_ping_scan(testScan.target_ip)
    assert ip_list[0].__contains__(testScan.get_default_gateway_ip())
