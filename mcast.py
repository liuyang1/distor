#! /usr/bin/python
# -*- coding: utf-8 -*-
import socket
import os

import logger
from conf import eConf
log = logger.get()

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(
            fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                                        ifname[:15]))[20:24])


def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0",
                      "ath0",
                      "ath1",
                      "ppp0",
                      ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


class McastSocket(socket.socket):

    def __init__(self, local_port, mcast_addr, mcast_iface, reuse=True):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM,
                               socket.IPPROTO_UDP)
        if(reuse):
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(("", local_port))
        try:
            self.setsockopt(socket.IPPROTO_IP,
                            socket.IP_ADD_MEMBERSHIP,
                            socket.inet_aton(mcast_addr)
                            + socket.inet_aton(mcast_iface))
        except socket.error:
            log.warning("add mcast failed "
                        + str(mcast_addr)
                        + " " + str(mcast_iface))
            raise socket.error
        self.dest = (mcast_addr, local_port)

    def publish(self, msg):
        self.sendto(msg, self.dest)

    def close(self):
        # 不需要显式的离开组播组,当相应套接字关闭的时候,该成员关系自动抹除
        # self.setsockopt(socket.IPPROTO_IP,
        #        socket.IP_DROP_MEMBERSHIP,
        #        socket.inet_aton(self.mcast_addr)
        #        + socket.inet_aton(self.mcast_iface))
        socket.socket.close(self)


eSock = McastSocket(eConf["mport"], eConf["maddr"], get_lan_ip())
