import struct
import time
import socket

TURN_ON_1 = 0x71
TURN_ON_2 = 0x23
TURN_ON_3 = 0x0f
TURN_OFF_1 = 0x71
TURN_OFF_2 = 0x24
TURN_OFF_3 = 0x0f
RESPONSE_LEN_POWER = 4

class Light(object):

    PORT = 5577

    def __init__(
            self,
            addr,
            port=PORT,
            name="None",
            confirm_receive_on_send=False,
            allow_fading=True):
        self.addr = addr
        self.port = port
        self.name = name
        self.is_on = False
        self.confirm_receive_on_send = confirm_receive_on_send
        self.allow_fading = allow_fading

        self._connect()
    
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.addr, self.port))

    def _send(self, data):
        return self._sock.send(data)

    def _receive(self, length):
        return self._sock.recv(length)
    
    def _calc_checksum(self, data):
        hex_checksum = hex(sum(data))
        checksum = int(hex_checksum[-2:], 16)
        return checksum

    def _attach_checksum(self, data):
        checksum = self._calc_checksum(data)
        return data + [checksum]

    def _send_with_checksum(self, data, response_len, receive=True):
        data_with_checksum = self._attach_checksum(data)
        format_str = '!%dB' % len(data_with_checksum)
        data = struct.pack(format_str, *data_with_checksum)
        self._send(data)
        if receive:
            response = self._receive(response_len)
            return response
    
    def _change_color(self, rgb_tuple, do_white = False):
        allow_white = 0xf0
        if(do_white):
            allow_white = 0x0f
            data = [0x31, 0, 0, 0, rgb_tuple[0], rgb_tuple[1], allow_white, 0x0f]
        else:
            data = [0x31, rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], 0, 0, allow_white, 0x0f]
        self._send_with_checksum(data, 1, False)
    
    def _turn_on(self):
        on_data = [TURN_ON_1, TURN_ON_2, TURN_ON_3]
        return self._send_with_checksum(
            on_data,
            RESPONSE_LEN_POWER,
            receive= False
        )
        self.is_on = True

    def _turn_off(self):
        off_data = [
            TURN_OFF_1,
            TURN_OFF_2,
            TURN_OFF_3
        ]
        return self._send_with_checksum(
            off_data,
            RESPONSE_LEN_POWER,
            receive = False
        )
        self.is_on = False
