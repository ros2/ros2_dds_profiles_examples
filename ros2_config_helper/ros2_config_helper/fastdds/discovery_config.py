from lxml import etree as ET

from ..dds_profiles import DDSProfilesFromDiscoveryConfig
from ..discovery_config import DiscoveryConfig
from ..discovery_config import DiscoveryType

FASTDDS_PROFILES_SCHEMA_URL = 'http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles'
FASTDDS_XML_NAMESPACES = {'': FASTDDS_PROFILES_SCHEMA_URL}
FASTDDS_INTERFACES_XPATH = './/interfaceWhiteList'
FASTDDS_INTERFACE_XML_ITEM = '<address>{}</address>'
FASTDDS_PEERS_PARENT_XPATH = './/builtin'
FASTDDS_PEERS_XML_TAG = 'initialPeersList'
FASTDDS_PEER_XML_ITEM = """
<locator>
    <udpv4>
        <address>{}</address>
    </udpv4>
</locator>
"""
FASTDDS_DISABLE_MULTICAST_PARENT_XPATH = './/builtin'
FASTDDS_DISABLE_MULTICAST_XML_ITEM = """
<metatrafficUnicastLocatorList>
    <locator/>
</metatrafficUnicastLocatorList>
"""
FASTDDS_PEER_RANGE_PARENT_XPATH = './/transport_descriptor'
FASTDDS_PEER_RANGE_XML_ITEM = '<maxInitialPeersRange>{}</maxInitialPeersRange>'

FASTDDS_BASE_XML_PROFILES = """\
<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
    <transport_descriptors>
        <transport_descriptor>
            <transport_id>udp_transport</transport_id>
            <type>UDPv4</type>
            <interfaceWhiteList>
            </interfaceWhiteList>
        </transport_descriptor>
    </transport_descriptors>

    <participant profile_name="default_part_profile" is_default_profile="true">
        <rtps>
            <builtin/>
            <useBuiltinTransports>false</useBuiltinTransports>
            <userTransports>
                <transport_id>udp_transport</transport_id>
            </userTransports>
        </rtps>
    </participant>
</profiles>
"""


class FastDDSProfilesFromDiscoveryConfig(DDSProfilesFromDiscoveryConfig):
    _BASE_XML_PROFILES = FASTDDS_BASE_XML_PROFILES
    _XML_NAMESPACES = FASTDDS_XML_NAMESPACES
    _INTERFACES_XPATH = FASTDDS_INTERFACES_XPATH
    _INTERFACE_XML_ITEM = FASTDDS_INTERFACE_XML_ITEM
    _PEERS_PARENT_XPATH = FASTDDS_PEERS_PARENT_XPATH
    _PEERS_XML_TAG = FASTDDS_PEERS_XML_TAG
    _PEER_XML_ITEM = FASTDDS_PEER_XML_ITEM
    _DISABLE_MULTICAST_PARENT_XPATH = FASTDDS_DISABLE_MULTICAST_PARENT_XPATH
    _DISABLE_MULTICAST_XML_ITEM = FASTDDS_DISABLE_MULTICAST_XML_ITEM
    _PEER_RANGE_PARENT_XPATH = FASTDDS_PEER_RANGE_PARENT_XPATH
    _PEER_RANGE_XML_ITEM = FASTDDS_PEER_RANGE_XML_ITEM
    _RMW_IMPLEMENTATION_NAME = 'rmw_fastrtps_cpp'
    _EXPORT_XML_PROFILE_FILE = 'export FASTRTPS_DEFAULT_PROFILES_FILE=$THIS_DIR/profiles.xml'
