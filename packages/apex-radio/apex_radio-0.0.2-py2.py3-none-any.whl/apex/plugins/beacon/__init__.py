# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import click

import apex.aprs.util

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []
__version__ = '0.0.2'

plugin = None


def start(config, port_map, packet_cache, aprsis):
    global plugin
    plugin = BeaconPlugin(config, port_map, packet_cache, aprsis)
    plugin.run()


def handle_packet(frame, recv_port, recv_port_name):
    return


def stop():
    plugin.stop()


class BeaconPlugin(object):

    def __init__(self, config, port_map, packet_cache, aprsis):
        self.port_map = port_map
        self.packet_cache = packet_cache
        self.aprsis = aprsis
        self.running = False

        for section in config.sections():
            if section.startswith('TNC '):
                tnc_name = section.split(' ')[1]
                for port_id in range(1, 1+int(config.get(section, 'port_count'))):
                    port_name = tnc_name + '-' + str(port_id)
                    port = port_map[port_name]
                    port_section = 'PORT ' + port_name
                    port['beacon_text'] = config.get(port_section, 'beacon_text')
                    port['beacon_path'] = config.get(port_section, 'beacon_path')

    def stop(self):
        self.running = False

    def run(self):
        self.running = True

        # Don't do anything in the first 30 seconds
        last_trigger = time.time()
        while self.running and time.time() - last_trigger < 30:
            time.sleep(1)

        # run every 600 second
        last_trigger = time.time()
        while self.running:
            if time.time() - last_trigger >= 600:
                last_trigger = time.time()
                for port_name in self.port_map.keys():
                    port = self.port_map[port_name]

                    beacon_frame = {'source': port['identifier'], 'destination': 'APRS',
                                    'path': port['beacon_path'].split(','), 'text': port['beacon_text']}
                    frame_hash = apex.aprs.util.hash_frame(beacon_frame)
                    if frame_hash not in self.packet_cache.values():
                        self.packet_cache[str(frame_hash)] = frame_hash
                        port['tnc'].write(beacon_frame, port['tnc_port'])
                        click.echo(port_name + ' >> ' + apex.aprs.util.encode_frame(beacon_frame))
            else:
                time.sleep(1)
