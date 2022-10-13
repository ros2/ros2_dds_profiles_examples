from lxml import etree as ET

from ..dds_profiles import DDSProfilesFromDiscoveryConfig
from ..discovery_config import DiscoveryConfig
from ..discovery_config import DiscoveryType

CYCLONEDDS_PROFILES_SCHEMA_URL = 'https://cdds.io/config'
CYCLONEDDS_XML_NAMESPACES = {'': CYCLONEDDS_PROFILES_SCHEMA_URL}
CYCLONEDDS_INTERFACES_XPATH = './/Interfaces'
CYCLONEDDS_INTERFACE_XML_ITEM = '<NetworkInterface address="{}" multicast="{}"/>'
CYCLONEDDS_PEERS_PARENT_XPATH = './/Discovery'
CYCLONEDDS_PEERS_XML_TAG = 'Peers'
CYCLONEDDS_PEER_XML_ITEM = """<Peer address="{}"/>"""
CYCLONEDDS_DISABLE_MULTICAST_PARENT_XPATH = './/General'
CYCLONEDDS_DISABLE_MULTICAST_XML_ITEM = """<AllowMulticast>false</AllowMulticast>"""
CYCLONEDDS_PEER_RANGE_PARENT_XPATH = './/Discovery'
CYCLONEDDS_PEER_RANGE_XML_ITEM = '<MaxAutoParticipantIndex>{}</MaxAutoParticipantIndex>'

CYCLONEDDS_BASE_XML_PROFILES = """\
<CycloneDDS xmlns="https://cdds.io/config" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://cdds.io/config https://raw.githubusercontent.com/eclipse-cyclonedds/cyclonedds/master/etc/cyclonedds.xsd">
    <Domain Id="any">
        <General>
            <Interfaces>
            </Interfaces>
        </General>
        <Discovery/>
    </Domain>
</CycloneDDS>
"""


class CycloneDDSProfilesFromDiscoveryConfig(DDSProfilesFromDiscoveryConfig):
    _BASE_XML_PROFILES = CYCLONEDDS_BASE_XML_PROFILES
    _XML_NAMESPACES = CYCLONEDDS_XML_NAMESPACES
    _INTERFACES_XPATH = CYCLONEDDS_INTERFACES_XPATH
    _INTERFACE_XML_ITEM = CYCLONEDDS_INTERFACE_XML_ITEM
    _PEERS_PARENT_XPATH = CYCLONEDDS_PEERS_PARENT_XPATH
    _PEERS_XML_TAG = CYCLONEDDS_PEERS_XML_TAG
    _PEER_XML_ITEM = CYCLONEDDS_PEER_XML_ITEM
    _DISABLE_MULTICAST_PARENT_XPATH = CYCLONEDDS_DISABLE_MULTICAST_PARENT_XPATH
    _DISABLE_MULTICAST_XML_ITEM = CYCLONEDDS_DISABLE_MULTICAST_XML_ITEM
    _PEER_RANGE_PARENT_XPATH = CYCLONEDDS_PEER_RANGE_PARENT_XPATH
    _PEER_RANGE_XML_ITEM = CYCLONEDDS_PEER_RANGE_XML_ITEM
    _RMW_IMPLEMENTATION_NAME = 'rmw_cyclonedds_cpp'
    _EXPORT_XML_PROFILE_FILE = 'export CYCLONEDDS_URI=file://$THIS_DIR/profiles.xml'

    @classmethod
    def _add_interface_item(cls, parent, address, discovery_type):
        multicast_flag = str(discovery_type is not DiscoveryType.Unicast).lower()
        parent.append(ET.fromstring(cls._INTERFACE_XML_ITEM.format(address, multicast_flag)))
