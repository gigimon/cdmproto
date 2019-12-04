import logging
import typing as tp

import serial

from . import consts


LOG = logging.getLogger(__name__)


class CDM:
    def __init__(self, dev: str, baund: int = 9600, timeout: int = 10):
        """
        Initialize device
        :param dev: path to com port
        """
        self._serial: tp.Optional[serial.Serial] = None
        self._device = dev
        self._baund = baund
        self._connect_timeout = timeout

    @property
    def term(self):
        if self._serial is None or not self._serial.is_open():
            self._serial = serial.Serial(self._device, baudrate=self._baund, timeout=self._connect_timeout)
        return self._serial

    def _send(self, data: bytes):
        LOG.debug(f'Send data: "{data}" to device')
        packet = self._build_packet(data)
        LOG.debug(f'Packet: "{packet}"')
        self.term.write(packet)

    def _ack(self):
        LOG.debug('Send ACK')
        self.term.write(bytes([consts.COMMANDS.ACK]))

    def _read(self) -> bytes:
        LOG.debug('Start read data')
        data = bytes()

        while True:
            data += self.term.read()
            LOG.debug(f'All data: "{data}"')

            if data == consts.COMMANDS.ACK or data[-2] == consts.COMMANDS.ETX:
                break
        if data != consts.COMMANDS.ACK:
            self._verify_packet(data)
        return data

    def _build_packet(self, data: bytes) -> bytes:
        LOG.debug('Build packet')
        data = bytes(len(data)) + data + consts.COMMANDS.ETX
        return consts.COMMANDS.STX + data + self.calc_bcc(data)

    def _verify_packet(self, data: bytes):
        LOG.debug(f'Verify packet: "{data}"')
        assert data[0] == consts.COMMANDS.STX
        assert data[-2] == consts.COMMANDS.ETX
        assert data[1] == len(data[2: -2])
        assert self.calc_bcc(data[1: -1]) == data[-1]

    def calc_bcc(self, data: bytes):
        LOG.debug(f'Calculate BCC for data: "{data}"')
        bcc = 0x00
        for b in data:
           bcc ^= b
        LOG.debug(f'Result BCC: "{bcc}"')
        return bcc

    def initialize(self):
        LOG.debug('Initialize device')
        self._send(consts.COMMANDS.INITIALIZE)
        data = self._read()
        self._send(bytes([0x05]))
        data = self._read()
        self._ack()

