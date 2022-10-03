from ipaddress import IPv4Address
import sys

try:
    import netifaces as ni
except ImportError:
    ni = None


def comma_separated_to_list(comma_separated):
    return [x.strip() for x in comma_separated.split(',')]


def check_valid_network_interface_or_address(network_interface_or_address, only_addresses=False):
    if ni is None and not only_addresses:
        raise RuntimeError(
            'netifaces is not available and required to check validity of interfaces')
    if only_addresses:
        return check_is_valid_ip_address(network_interface_or_address)
    if network_interface_or_address in ni.interfaces():
        return True
    addresses = [
        ni.ifaddresses(interface)[ni.AF_INET][0]['addr'] for interface in ni.interfaces()
        if ni.AF_INET in ni.ifaddresses(interface) and
        len(ni.ifaddresses(interface)[ni.AF_INET]) == 1
    ]
    if not network_interface_or_address in addresses:
        print(f'[{network_interface_or_address}] is not a valid network interface', file=sys.stderr)
        return False
    return True


def check_valid_network_interfaces_or_addresses(network_interfaces_or_addresses, only_addresses=False):
    network_interfaces_or_addresses_list = comma_separated_to_list(
        network_interfaces_or_addresses)
    # run the check through all items, to make sure we log all the incorrect ones
    results = [
        check_valid_network_interface_or_address(interface_or_address, only_addresses)
        for interface_or_address in network_interfaces_or_addresses_list
    ]
    return all(results)


def to_address(network_interface_or_address, only_addresses=False):
    if ni is None and not only_addresses:
        raise RuntimeError(
            'netifaces is not available and required to check validity of interfaces')
    if only_addresses or not network_interface_or_address in ni.interfaces():
        # do not check, assume check_valid_network_interface_or_address() was used before
        return network_interface_or_address
    interface = network_interface_or_address
    interface_ifaddresses = ni.ifaddresses(interface)
    if not ni.AF_INET in interface_ifaddresses:
        raise RuntimeError(f'interface [{interface}] does not have a IPv4 address')
    addresses = interface_ifaddresses[ni.AF_INET]
    if len(addresses) != 1:
        raise RuntimeError(
            f'Expected interface [{interface}] does not have an unique IPv4 address,'
            ' specify one of its ip instead')
    return addresses[0]['addr']


def to_addresses(network_interfaces_or_addresses, only_addresses=False):
    network_interfaces_or_addresses_list = comma_separated_to_list(
        network_interfaces_or_addresses)
    return [
        to_address(network_interface_or_address, only_addresses) for network_interface_or_address
        in network_interfaces_or_addresses_list
    ]


def check_is_valid_ip_address(address):
    try:
        IPv4Address(address)
    except ValueError:
        print(f'[{address}] is not a valid ip address')
        return False
    return True


def check_is_valid_ip_addresses(addresses):
    addresses_list = comma_separated_to_list(addresses)
    # run the check through all items, to make sure we log all the incorrect ones
    results = [
        check_is_valid_ip_address(address)
        for address in addresses_list
    ]
    return all(results)
