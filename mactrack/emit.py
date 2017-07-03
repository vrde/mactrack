import json
import subprocess
import threading
import time
import uuid

import logging

from dateutil import parser

from . import db


log = logging.getLogger(__name__)


def parse():
    proc = subprocess.Popen('tshark -i mon0 -Tjson -ta subtype probereq 2> /dev/null',
                            shell=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    log.debug('tshark started, waiting for new probe requests')

    buf = None
    for line in proc.stdout:
        if line.startswith('['):
            pass
        elif line.startswith('  {'):
            buf = []
            buf.append(line)
        elif line.startswith('  }'):
            buf.append(line)
            layers = json.loads(''.join(buf))['_source']['layers']
            layers['frame']['frame.time'] = parser.parse(layers['frame']['frame.time'])
            layers['wlan_radio']['wlan_radio.signal_dbm'] = int(layers['wlan_radio']['wlan_radio.signal_dbm'])
            yield layers
        else:
            buf.append(line)

TOTAL = 0

def talk():
    while True:
        subprocess.call(['espeak', 'Total beacons {}'.format(TOTAL)])
        time.sleep(10)


def run():
    global TOTAL
    # threading.Thread(target=talk).start()
    conn = db.get_conn()

    for packet in parse():
        id_ = str(uuid.uuid4())
        dt = packet['frame']['frame.time'].isoformat()
        dbm = packet['wlan_radio']['wlan_radio.signal_dbm']
        sa = packet['wlan']['wlan.sa']
        sa_resolved = packet['wlan']['wlan.sa_resolved']
        log.debug('New probe request from %s (%sdbm)', sa_resolved, dbm)
        db.insert_beacon(conn, id_, dt, dbm, sa, sa_resolved, 52.5200, 13.4050)
        TOTAL += 1
