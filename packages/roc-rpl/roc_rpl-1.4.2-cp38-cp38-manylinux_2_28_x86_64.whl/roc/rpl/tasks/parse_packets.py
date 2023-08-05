#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from poppy.core.logger import logger
    from poppy.core.task import Task
    from poppy.core.target import PyObjectTarget
    from poppy.core.tools.exceptions import MissingInput
except:
    print('POPPy framework is not installed!')

from roc.rpl import VALID_PACKET
from roc.rpl.exceptions import PacketParsingError
from roc.rpl.time import Time
from roc.rpl.packet_parser.packet_parser import PacketParser

__all__ = ['ParsePackets']

@PyObjectTarget.input(identifier='raw_data')
@PyObjectTarget.output(identifier='raw_data')
@Task.as_task(plugin_name='roc.rpl', name='parse_packets')
def ParsePackets(task):
    """
    To make the RPW TM/TC packet parsing as a task.

    :param task: input task object.
    :return:
    """

    try:
        raw_data = task.inputs['raw_data'].value
    except:
        raise MissingInput('raw_data input is missing')

    # Get/create Time instance for time computation
    time_instance = Time()

    # Get IDB inputs
    idb_version = task.pipeline.get('idb_version', default=[None], args=True)[0]
    if idb_version is None:
        idb_version = raw_data.idb_version
    idb_source = task.pipeline.get('idb_source', default=[None], args=True)[0]
    if idb_source is None:
        idb_source = raw_data.idb_source

    # Pass input arguments for the Time instance
    time_instance.kernel_date = task.pipeline.get('kernel_date', default=None, args=True)
    time_instance.predictive = task.pipeline.get('predictive', default=True, args=True)
    time_instance.no_spice = task.pipeline.get('no_spice', default=False, args=True)

    # Initialize packet parser
    parser = PacketParser(
            idb_version=idb_version,
            idb_source=idb_source,
            time=time_instance,
        )

    # Get start-time
    start_time = task.pipeline.get('start_time', default=[None])[0]

    # Get end-time
    end_time = task.pipeline.get('end_time', default=[None])[0]

    # connect to add exception when packet analysis is bad
    parser.extract_error.connect(task.exception)

    # Analyse input RPW TM/TC packets
    logger.info(f'Extracting data from {len(raw_data.packet_list)} input packet(s)...')
    try:
        identified_packet_list = parser.parse_packets(raw_data.packet_list,
                          start_time=start_time,
                          end_time=end_time,
                          valid_only=False)

    except:
        raise PacketParsingError('Packet parsing has failed!')
    else:
        # Fill raw_data packet list
        raw_data.packet_list = [current_packet
                                for current_packet in identified_packet_list
                                if current_packet['status'] == VALID_PACKET]
        raw_data.invalid_packet_list = [current_packet
                                for current_packet in identified_packet_list
                                if current_packet['status'] != VALID_PACKET]
        raw_data.packet_parser = parser


    # store the raw_data instance into the properties
    task.outputs['raw_data'].value = raw_data
