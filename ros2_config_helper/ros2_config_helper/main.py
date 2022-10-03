from pathlib import Path
import sys
import time

import argparse
from lxml import etree as ET

from .cyclonedds.discovery_config import cyclonedds_profiles_from_discovery_config
from .discovery_config import create_discovery_config_from_questions
from .discovery_config import DiscoveryConfig
from .discovery_config import DiscoveryType
from .fastdds.discovery_config import fastrtps_profiles_from_discovery_config

BACKENDS = {
    'fastdds': fastrtps_profiles_from_discovery_config,
    'cyclonedds': cyclonedds_profiles_from_discovery_config,
}


def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Tool to configure ROS 2 DDS vendors')
    parser.add_argument(
        '--backends', '-b', nargs='*', choices=('all', *BACKENDS.keys()), default=['all'],
        help='DDS vendor specific backend to use, if "all" is selected every backend will be run')
    parser.add_argument(
        '--output-dir', '-o', type=Path, default=Path(f'ros2_config_helper_{time.time_ns()}'))
    return parser.parse_args(argv)


def print_mkdir_error(exc, output_dir):
    base_msg = f"Cannot create directory '{output_dir}': "
    if isinstance(exc, FileNotFoundError):
        end = 'parent directory does not exist'
    elif isinstance(exc, FileExistsError):
        end = 'directory already exists'
    else:
        end = str(exc)
    print(f'{base_msg}{end}', file=sys.stderr)


def main(args):
    output_dir = args.output_dir.resolve()
    try:
        output_dir.mkdir(mode=0o775)
    except Exception as exc:
        print_mkdir_error(exc, output_dir)
        return 1
    discovery_config = create_discovery_config_from_questions()
    backends = args.backends
    print(args.backends)
    if 'all' in args.backends:
        backends = BACKENDS.keys()
    print(backends)
    for backend_name in backends:
        print(backend_name)
        backend_output_dir = output_dir / backend_name
        try:
            backend_output_dir.mkdir(mode=0o775)
        except Exception as exc:
            print_mkdir_error(exc, backend_output_dir)
            return 1
        output_file = backend_output_dir / 'profiles.xml'
        try:
            output_file.open('x')
        except Exception as exc:
            print(
                f"Unexpected error when opening file: {exc}",
                file=sys.stderr)
            return 1
        backend = BACKENDS[backend_name]
        try:
            xml_element = backend(discovery_config)
            et = ET.ElementTree(xml_element)
            et.write(output_file, encoding='unicode')
        except Exception as exc:
            print(
                'Unexpected error when generating XML profiles for backend '
                f"{backend_name}': {exc}",
                file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(parse_args()))
