#! /usr/bin/python
# -*- coding: utf-8 -*-
import socket

import logger
log = logger.get()


class McastSocket(socket.socket):

    def __init__(self, local_port, reuse=False):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM,
                               socket.IPPROTO_UDP)
        if(reuse):
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(("", local_port))

    def mcast_add(self, mcast_addr, mcast_iface):
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
        self.mcast_addr = mcast_addr
        self.mcast_iface = mcast_iface

    def close(self):
        # 不需要显式的离开组播组,当相应套接字关闭的时候,该成员关系自动抹除
        # self.setsockopt(socket.IPPROTO_IP,
        #        socket.IP_DROP_MEMBERSHIP,
        #        socket.inet_aton(self.mcast_addr)
        #        + socket.inet_aton(self.mcast_iface))
        socket.socket.close(self)
