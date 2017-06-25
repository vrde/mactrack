# Introduction

`mactrack` is a proof of concept to track who is around.

In order to discover new WiFi networks, smartphones do a couple of things:
 - They passively listen to beacons from the surrounding networks
 - They actively send beacons asking if there are WiFi networks around.

Each beacon carries a unique identifier: the `MAC` address of the network
interface inside your smartphone.

Track `MAC` addresses means **track people**.

`mactrack` listens to those beacons smartphones constantly send.

Right now `mactrack` is just a dumb python script that parses data
coming from another program (`tshark`). The next step is to store those beacons
in a database and start analyzing this data.


## Why?

I'm doing this to show how easy is to implement this surveillance pattern, and
how our privacy is constantly compromised.

While my approach is pretty basic, a more sophisticated implementation **and**
a large scale deployment can help:
 - Governments, to see who's taking part of a demo/protest, or to "simply" track
 how people move around.
 - Burglars, to check if you are at home or not.
 - Private companies, to track people in their stores.
 - ...


# Setup for Ubuntu

(Works also with Ubuntu-based Raspberry Pi)


## Disable NetworkManager for specific interfaces
To avoid `NetworkManager` to interfere with your monitoring interface,
you need to blacklist it.

Open `/etc/NetworkManager/NetworkManager.conf`, add:

```
[keyfile]
unmanaged-devices=interface-name:wlan1
```

Or, if you want to disable an interface using its mac address:

```
[keyfile]
unmanaged-devices=mac:00:11:22:33:44:55
```

## Put the interface in monitor mode

Install `aircrack-ng`, then:
```
# airmon-ng start <wlan-name>
```

This will create a new interface called (usually) `mon0`.

## Start `airodump-ng`

```
# airodump-ng mon0
```

If the setup was successful, the `nic` should start hopping between
different channels and show the mac addresses of the devices around.

## Play with `tshark`

Install `tshark`, run:

```
tshark -i mon0 subtype probereq
```
