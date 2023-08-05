#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

import pytest

from poppy.core.test import CommandTestCase
from roc.rpl.packet_structure.header import Header, TMHeader
from roc.rpl.packet_parser import PacketParser
from roc.rpl import Time

class TestIdentifyPacket(CommandTestCase):
    """
    Test the identify_packet() method in packet_parser.
    """

    @pytest.mark.parametrize(
        'idb_source,idb_version',
        [('MIB', '20200113'),],
    )
    def test_identify_packet(self, idb_source, idb_version):

        # initialize the IDB

        # Db migration
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'INFO']

        # IDB PALISADE loading
        idb_palisade_loading = [
            'pop',
            'idb',
            'install',
            '-s',
            'PALISADE',
            '-v',
            '4.3.5_MEB_PFM',
            '--load',
            '-ll',
            'INFO',
        ]

        # IDB MIB loading
        idb_mib_loading = [
            'pop',
            'idb',
            'install',
            '-s',
            idb_source,
            '-v',
            idb_version,
            '--load',
            '-ll',
            'INFO',
        ]

        # apply database migrations
        self.run_command(db_upgrade)

        # Apply IDB loading
        self.run_command(idb_palisade_loading)

        # Apply IDB loading
        self.run_command(idb_mib_loading)

        # Generate input for identify_packet
        input = {'type': 'TM',
                'srdb_id': None,
                'palisade_id': None,
                'binary': '0CB7D904000D100501002730B9A4E54FA6D20165'}

        # Generate expected output
        expected_output = {'type': 'TM',
               'srdb_id': 'YIW00073',
               'palisade_id': 'TM_DPU_EVENT_PR_DPU_MODE',
               'binary': '0CB7D904000D100501002730B9A4E54FA6D20165',
               'comment': '',
               'idb_source': 'MIB',
               'idb_version': '20200131',
               'header': Header(0, 0, 1, 75, 7, 3, 6404, 13),
               'data_header': TMHeader(0, 1, 0, 5, 1, 0, (657504676, 58703, 0)),
               'apid': 1207,
               'category': '/RPW/Telemetry/DPU_PROCESS/Progress Event Reporting',
               'scet': 657504676.8957367,
               'utc_time': datetime.datetime(2020, 11, 1, 0, 11, 54, 642361),
               'sync_flag': True,
               'obt_time': '1/657504676:58703',
               'sha': '564d9e91b40e1f49ac17b3dcc72c3adb69ff760e06aff158a27aaa2bf27b1287',
               'length': 20,
               'status': 0}


        # Instantiate the packet parser
        packet_parser = PacketParser(
            idb_version=idb_version,
            idb_source=idb_source,
            time=Time(),
        )

        # connect to add exception when packet analysis is bad
        packet_parser.extract_error.connect(self.exception)

        # Analyse input RPW TM/TC packets
        packet_parser.parse_packets([input])

        print(packet_parser.parsed_packets[0])
        print(expected_output)

        # Check output versus expected output
        assert packet_parser.parsed_packets[0] == expected_output
