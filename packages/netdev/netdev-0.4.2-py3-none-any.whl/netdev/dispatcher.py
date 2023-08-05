"""
Factory function for creating netdev classes
"""
from .cisco import CiscoAsa
from .cisco import CiscoIos
from .cisco import CiscoNxos
from .hp import HPComware
from .fujitsu import FujitsuSwitch
from .mikrotik import MikrotikRouterOS

# @formatter:off
# The keys of this dictionary are the supported device_types
CLASS_MAPPER = {
    'cisco_ios': CiscoIos,
    'cisco_xe': CiscoIos,
    'cisco_asa': CiscoAsa,
    'cisco_nxos': CiscoNxos,
    'hp_comware': HPComware,
    'fujitsu_switch': FujitsuSwitch,
    'mikrotik_routeros': MikrotikRouterOS,
}

# @formatter:on

platforms = list(CLASS_MAPPER.keys())
platforms.sort()
platforms_str = u"\n".join(platforms)


def create(*args, **kwargs):
    """Factory function selects the proper class and creates object based on device_type"""
    if kwargs['device_type'] not in platforms:
        raise ValueError('Unsupported device_type: '
                         'currently supported platforms are: {0}'.format(platforms_str))
    connection_class = CLASS_MAPPER[kwargs['device_type']]
    return connection_class(*args, **kwargs)
