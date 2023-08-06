#!/usr/bin/python

# 2013-09-02 Aprogas

# 2015-12-12 Duality:
# class structure introduced for easy implentation of other
# protocols, and abstraction of sockets.
from DeviceInterfaces import UdpSocket
from Filter import convert_snake_layout
from Filter import convert_dim_layout


class Artnet(UdpSocket):
    def __init__(self, universe=0, port=6454):
        UdpSocket.__init__(self, port=port)
        self.universe = universe

    def build_packet(self, universe, dmxdata):
        # based on fire-ohmlogo.py by OHM 2013
        # 3 * 1024 because r + g + b == 3 colors
        size = len(dmxdata) * 3
        if size >= (1024 - 18):
            raise(Exception("dmxdata to big to fit packet."))
        #              01234567   8   9   a   b   c   d   e   f   10  11
        #                         op-code protver seq phy universe len
        data = bytearray("Art-Net\x00\x00\x50\x00\x0e\x00\x00")
        data += chr(int(universe % 256))
        data += chr(int(universe / 256))
        data += chr(int(size / 256))
        data += chr(int(size % 256))
        data += str(dmxdata)
        return data

    def send(self, data, ip):
        data = self.build_packet(self.universe, data)
        self.transmit(data, ip)


class Pixelmatrix(Artnet):
    """
        enable snake mode and flip x for pixelmatrix
    """

    def __init__(self, universe=0, port=6454):
        Artnet.__init__(self, universe, port)

    def send(self, data, ip):
        data = convert_dim_layout(data)
        data = convert_snake_layout(data)
        data = self.build_packet(self.universe, data)
        self.transmit(data, ip)
