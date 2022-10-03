from typing import Dict

from lxml import etree as ET

from .discovery_config import DiscoveryConfig
from .discovery_config import DiscoveryType


class DDSProfilesFromDiscoveryConfig:
    _BASE_XML_PROFILES: str
    _XML_NAMESPACES: Dict[str, str]
    _INTERFACES_XPATH: str
    _INTERFACE_XML_ITEM: str
    _PEERS_PARENT_XPATH: str
    _PEERS_XML_TAG: str
    _PEER_XML_ITEM: str
    _DISABLE_MULTICAST_PARENT_XPATH: str
    _DISABLE_MULTICAST_XML_ITEM: str
    _PEER_RANGE_PARENT_XPATH: str
    _PEER_RANGE_XML_ITEM: str
  
    @classmethod
    def _check_valid_config(cls, discovery_config: DiscoveryConfig):
        discovery_types = set(discovery_config.network_interfaces_to_discovery_type.values())
        if not len(discovery_types) == 1:
            raise RuntimeError('Must use the same discovery type in all interfaces')
        discovery_type = next(iter(discovery_types))
        if discovery_type == DiscoveryType.Both:
            # Double check, I think FastDDS may actually support this
            raise RuntimeError('Can only pick between multicast and unicast, not choose both')
    
    @classmethod
    def _add_interface_item(cls, parent, address, discovery_type):
        parent.append(ET.fromstring(cls._INTERFACE_XML_ITEM.format(address)))
    
    @classmethod
    def _add_disable_multicast_item(cls, root, network_interfaces_to_discovery_type):
        discovery_types = set(network_interfaces_to_discovery_type.values())
        is_multicast_not_used = all(
            discovery_type is DiscoveryType.Unicast for discovery_type in discovery_types)
        if is_multicast_not_used:
            disable_multicast_parent = root.find(
                cls._DISABLE_MULTICAST_PARENT_XPATH, cls._XML_NAMESPACES)
            disable_multicast_parent.append(ET.fromstring(cls._DISABLE_MULTICAST_XML_ITEM))
        
    @classmethod
    def profiles_from_discovery_config(
        cls,
        discovery_config: DiscoveryConfig,
    ) -> ET.Element:
        profiles_file = ET.fromstring(cls._BASE_XML_PROFILES)
        cls._check_valid_config(discovery_config)
        interfaces_element = profiles_file.find(cls._INTERFACES_XPATH, cls._XML_NAMESPACES)
        for address, discovery_type in discovery_config.network_interfaces_to_discovery_type.items():
            cls._add_interface_item(interfaces_element, address, discovery_type)
        if discovery_config.initial_peers:
            peers_parent = profiles_file.find(cls._PEERS_PARENT_XPATH, cls._XML_NAMESPACES)
            peers = ET.SubElement(peers_parent, cls._PEERS_XML_TAG)
            for peer_addr in discovery_config.initial_peers:
                peers.append(ET.fromstring(cls._PEER_XML_ITEM.format(peer_addr)))
        if discovery_config.peer_range is not None:
            peer_range_parent = profiles_file.find(cls._PEER_RANGE_PARENT_XPATH, cls._XML_NAMESPACES)
            peer_range_parent.append(
                ET.fromstring(cls._PEER_RANGE_XML_ITEM.format(discovery_config.peer_range)))
        cls._add_disable_multicast_item(
            profiles_file, discovery_config.network_interfaces_to_discovery_type)
        ET.indent(profiles_file)
        return profiles_file
