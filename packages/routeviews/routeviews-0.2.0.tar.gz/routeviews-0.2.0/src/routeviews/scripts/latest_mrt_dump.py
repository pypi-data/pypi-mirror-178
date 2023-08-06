"""Get metrics about the latest MRT Dump files on a Route Views collector.

TODO: Consider feature to monitor all MRT files on archive.routeviews.org.
"""
import logging
import os
import socket
import sys

import configargparse
import uologging

import routeviews.influx
from routeviews.filesystem import FileMetrics, latest_file, list_dir
from routeviews.types import MRTTypes

DEFAULT_MRT_PATH = '/mnt/storage/bgpdata/'

uologging.init_syslog()

logger = logging.getLogger(__name__)


def run_main():
    _main(sys.argv)


def _main(argv):
    """Parse args, set up logging, then call the inner 'main' function. 
    """
    package_name = __name__.split('.')[0]
    uologging.init_console(package_name)
    args = parse_args(argv)
    uologging.set_logging_verbosity(args.verbosity_flag, package_name)
    main(args)


def main(args):
    try:
        latest_RIB_path = latest_MRT_file(MRTTypes.RIBS, args.path)
        latest_UPDATE_path = latest_MRT_file(MRTTypes.UPDATES, args.path)
    except OSError as e:
        print(e)
        exit(1)
    if args.influxdb:
        print(
            generate_influxdb_line(
                collector=socket.gethostname(),
                latest_RIB=FileMetrics(latest_RIB_path),
                latest_update=FileMetrics(latest_UPDATE_path),
            )
        )
    elif args.simple:
        print(f'Latest RIB:    {latest_RIB_path}')
        print(f'Latest UPDATE: {latest_UPDATE_path}')
    else:
        print_detailed(latest_RIB_path, latest_UPDATE_path)


def print_detailed(latest_RIB_path: str, latest_UPDATE_path: str):
    import textwrap
    latest_RIB_stats = FileMetrics(latest_RIB_path).pprint()
    print('Latest RIB:')
    print(textwrap.indent(latest_RIB_stats, '  '))
    latest_update_stats = FileMetrics(latest_UPDATE_path).pprint()
    print('Latest UPDATE:')
    print(textwrap.indent(latest_update_stats, '  '))


def latest_MRT_file(mrt_type: MRTTypes, path=DEFAULT_MRT_PATH) -> str:
    """Gets the latest MRT file from a collector.

    Args:
        mrt_type: Choose which type of Route Views MRT file to lookup. RIB, 
        UPDATE path (str, optional): The path where Route Views MRT dumps 
        are stored. Defaults to DEFAULT_MRT_PATH.

    Returns:
        str: Path to the latest "mrt_type" file.
    """
    mrt_directories = list_dir(path, sort_key=os.path.getctime)
    for mrt_dir in mrt_directories:
        try:
            return latest_file(os.path.join(mrt_dir, mrt_type.name))
        except OSError:
            continue  # Try the next mrt_directory
    raise OSError(f'Unable to find files at: "{path}"')


def generate_influxdb_line(collector: str,
                           latest_RIB: FileMetrics,
                           latest_update: FileMetrics,
                           measurement='latest_mrt_dump'):
    """Generate a InfluxDB Line Protocol line.

    Args:
        hostname (str): Name of this collector that is sending data.
        latest_RIB (FileMetrics): Latest MRT RIB file. 
        latest_update (FileMetrics): Latest MRT UPDATE file.
        measurement (str, optional): Name of measurement in InfluxDB. 
        Defaults to 'latest_mrt_dump'.

    Returns:
        str: Single long string containing metrics we want to track.
    """
    return routeviews.influx.measurement_line(
        measurement,
        tags={
            'collector': collector,
        },
        fields={
            'RIB_file': latest_RIB.name,
            'RIB_age_sec': latest_RIB.age_in_seconds(),
            'RIB_size': latest_RIB.size,
            'update_file': latest_update.name,
            'update_age_sec': latest_update.age_in_seconds(),
            'update_size': latest_update.size,
        }
    )


def parse_args(argv):
    parser = configargparse.ArgumentParser(description=__doc__)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '--path', '-p',
        default=DEFAULT_MRT_PATH,
        help=f'Look for Route Views style MRT Archives at this path. Default: {DEFAULT_MRT_PATH}'
    )
    output_options = parser.add_mutually_exclusive_group()
    output_options.add_argument(
        '--influxdb',
        '-i',
        action='store_true',
        help='Produce a measurement as InfluxDB Line Protocol.'
    )
    output_options.add_argument(
        '--simple',
        '-s',
        action='store_true',
        help='Produce more detailed output, focused on being human readable.'
    )
    args = parser.parse_args(argv[1:])
    # Do any argument pre-processing. E.g. convert strings to objects.
    return args


if __name__ == '__main__':
    logger.warning(f'Invoked as script, not using entry point {__file__}')
    run_main()
