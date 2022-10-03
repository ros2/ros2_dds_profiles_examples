from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from ros2_config_helper import net_helper

class DiscoveryType(Enum):
    Unicast = 0
    Multicast = 1
    # This doesn't seem to be well supported in CycloneDDS, double check FastDDS
    Both = 2

@dataclass
class DiscoveryConfig:
    # FastDDS and CycloneDDS are both limited to use the same DiscoveryType for all
    # interfaces, combining unicast/multicast discovery in different interfaces doesn't seem
    # to work well.
    # Anyway, we make this more flexible to future-proof it.
    network_interfaces_to_discovery_type: Dict[str, DiscoveryType]
    initial_peers: Optional[List[str]] = None
    peer_range: Optional[int] = None


def get_validated_input(msg, validation, try_again_msg):
    input_data = input(msg)
    while not validation(input_data):
        input_data = input(try_again_msg)
    return input_data


def create_discovery_config_from_questions():
    print(
        'Select what describes best your use case:\n'
        '  - (A) Communication is limited to localhost, e.g. development.\n'
        '  - (B) Want to only discover local nodes by default, but be able to\n'
        '    connect from another computer if specifying the ip.\n'
        '    This will use unicast discovery.\n'
        '  - (C) Want to be able to talk to one or many other computers of\n'
        '    known IP(s). Discovery can be asymmetric, i.e. as long as all\n'
        '    nodes specify the IP of a common node, all nodes will be\n'
        '    communicated.\n'
        '  - (D) Want to use multicast discovery.')
    choice = get_validated_input(
        'pick one of (A/B/C/D): ',
        lambda choice: choice in ['A', 'B', 'C', 'D'],
        'input must be one of A/B/C/D, try again: ')
    print(f'choice: {choice}')
    if choice == 'A':
        return DiscoveryConfig(
            network_interfaces_to_discovery_type={'127.0.0.1': DiscoveryType.Multicast})
    print(
        'Select the network interfaces you want ROS 2 to use, you can use\n'
        'a comma separated list of IP addresses or interfaces names')
    network_interfaces_or_addresses = get_validated_input(
        'interfaces: ',
        net_helper.check_valid_network_interfaces_or_addresses,
        'all the interfaces need to be valid: ')
    network_interfaces_addresses = net_helper.to_addresses(network_interfaces_or_addresses)
    if '127.0.0.1' not in network_interfaces_addresses:
        # TODO: Check if there's a valid loopback interface
        network_interfaces_addresses.append('127.0.0.1')
    peers = []
    if choice == 'C':
        peers = get_validated_input(
            'Introduce the initial peer(s) IP address(es), comma separated: ',
            net_helper.check_is_valid_ip_addresses,
            'Addresses must be valid IPv4, try again: ')
        peers = net_helper.comma_separated_to_list(peers)
    discovery_type = DiscoveryType.Unicast if choice not in ['A', 'D'] else DiscoveryType.Multicast
    print(discovery_type)
    network_interfaces_to_discovery_type = {
        address: discovery_type for address in network_interfaces_addresses
    }
    peer_range = None
    if discovery_type in [DiscoveryType.Unicast, DiscoveryType.Both]:
        peers.append('127.0.0.1')
        print(
            'Introduce the maximum number of DDS participant (one per ROS 2 \n'
            'context, generally one per process) that will run in a single host.\n'
            'This will limit the range of ports used to try unicast discovery.'
        )
        def to_int(n):
                try:
                    return isinstance(int(n), int)
                except ValueError: 
                    return False
        get_validated_input(
            'Maximum number of participants in a host: ',
            to_int,
            'Please introduce an integer: ')
    return DiscoveryConfig(
        network_interfaces_to_discovery_type=network_interfaces_to_discovery_type,
        initial_peers=peers,
        peer_range=peer_range)
