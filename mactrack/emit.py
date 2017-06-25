import json
import subprocess

from dateutil import parser


def parse():
    proc = subprocess.Popen('tshark -i mon0 -Tjson -ta subtype probereq 2> /dev/null',
                            shell=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
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


def run():
    for packet in parse():
        time = packet['frame']['frame.time']
        signal = packet['wlan_radio']['wlan_radio.signal_dbm']
        sa = packet['wlan']['wlan.sa']
        sa_resolved = packet['wlan']['wlan.sa_resolved']
        print(time, signal, sa, sa_resolved)
