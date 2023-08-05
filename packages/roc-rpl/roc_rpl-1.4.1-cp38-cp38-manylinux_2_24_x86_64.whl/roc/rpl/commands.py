#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from poppy.core.command import Command
except:
    print('POPPy framework is not installed!')

__all__ = ['RPL']


class RPL(Command):
    """
    A command to do the decommutation of a test log file in the XML format.
    """
    __command__ = 'rpl'
    __command_name__ = 'rpl'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = (
        'Commands relative to the decommutation of packets with help ' +
        'of PacketParser library'
    )
