import os
import pathlib

import pytest
from auto_nmap import __version__
from auto_nmap.discoverDevices import get_default_gateway_ip, ip_to_ip_range
from mock import Mock

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..',))
OUTPUT_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'auto_nmap/txt-files/'))

mocker = Mock()


def test_version():
    assert __version__ == '0.1.0'


"""Start testing of discoverDevices.py"""


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


def test_output_ips_to_text_file(script_runner):
    script_runner.run('discoverDevices', '--output', 'test.txt')
    """Check if the output file exists."""
    file = pathlib.Path(OUTPUT_DIR + "/test.txt")
    assert file.exists()
