import time
import logging
import typing as tp

import serial

from . import consts, exceptions


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
        if self._serial is None or not self._serial.is_open:
            self._serial = serial.Serial(self._device, baudrate=self._baund, timeout=self._connect_timeout)
        return self._serial

    def _to_bytes(self, data: tp.Union[bytes, bytearray, list, tuple, int]) -> bytes:
        if isinstance(data, bytes):
            return data
        elif isinstance(data, int):
            return bytes([data])
        else:
            return bytes(data)

    def _to_hex(self, data: bytes) -> tp.List[str]:
        return [hex(i) for i in data]

    def send(self, data: tp.Union[int, list, bytes, bytearray]):
        LOG.debug(f'Send data: "{data}" to device')
        packet = self._to_bytes(data)
        if packet[0] not in [consts.COMMANDS.ACK, consts.COMMANDS.ENQ]:
            packet = self._build_packet(data)
        LOG.debug(f'Send packet: "{self._to_hex(packet)}"')
        self.term.write(packet)

    def ack(self):
        LOG.debug('Send ACK')
        self.term.write(bytes([consts.COMMANDS.ACK]))

    def read(self, verify: bool = False) -> bytes:
        LOG.debug('Start read data')
        data = bytes()
        LOG.debug(f'Check if buffer has data: "{self.term.in_waiting}/{self.term.out_waiting}"')
        while True:
            data += self.term.read()
            LOG.debug(f'Read from socket: {data}')
            if not data:
                time.sleep(1)
                continue
            if data[0] == consts.COMMANDS.ACK:
                self.send(bytes([consts.COMMANDS.ENQ]))
                data = bytes()
                continue

            if len(data) > 2 and data[-2] == consts.COMMANDS.ETX:
                break
            time.sleep(0.1)
        if data[0] != consts.COMMANDS.ACK and verify:
            self._verify_packet(data)  #Check why all responses has invalid bcc
        if self.term.in_waiting:
            self.term.read_all()
        LOG.debug(f'All readed data: {self._to_hex(data)}')
        return data

    def _build_packet(self, data: bytes) -> bytes:
        data = self._to_bytes(data)
        LOG.debug(f'Build packet for data: "{self._to_hex(data)}"')
        data = bytes([len(data)]) + data + bytes([consts.COMMANDS.ETX])
        return bytes([consts.COMMANDS.STX]) + data + self.calc_bcc(data)

    def _verify_packet(self, data: bytes):
        LOG.debug(f'Verify packet: "{data}"')
        assert data[0] == consts.COMMANDS.STX
        assert data[-2] == consts.COMMANDS.ETX
        assert data[1] == len(data[2: -2])
        assert self.calc_bcc(data[1: -1]) == data[-1]

    def calc_bcc(self, data: bytes) -> bytes:
        LOG.debug(f'Calculate BCC for data: "{self._to_hex(data)}"')
        bcc = 0x00
        for b in data:
           bcc ^= b
        LOG.debug(f'Result BCC: "{bcc}"')
        return bytes([bcc])

    def initialize(self):
        """Initialize device on first start (or after shutdown)"""
        LOG.debug('Initialize device')
        self.send(consts.COMMANDS.INITIALIZE)
        self.read()
        self.ack()

    def get_status(self):
        LOG.debug('Read device status')
        self.send(consts.COMMANDS.READ_STATUS)
        result = self.read()
        self.ack()
        if result[3] != consts.ERROR_CODES.NORMAL:
            raise exceptions.CDMError(f'Device has error: {result[3]}')
        return result

    def get_last_status(self):
        LOG.debug('Read last status')
        self.send(consts.COMMANDS.LAST_STATUS)
        result = self.read()
        self.ack()

    def diagnostic(self):
        LOG.debug('Diagnostic device')
        self.send(consts.COMMANDS.DIAGNOSTIC)
        result = self.read()
        self.ack()
        if result[3] != consts.ERROR_CODES.NORMAL:
            raise exceptions.CDMError(f'Device has error: {result[3]}')
        return result

    def dispense_bill(self, cassete_num: int, count: int):
        LOG.debug(f'Dispense bill "{cassete_num} for "{count}" banknotes')  #TODO: Add error handler
        self.send([consts.COMMANDS.DISPENSE_BILL, cassete_num, count])
        result = self.read()
        self.ack()
        if result[3] != consts.ERROR_CODES.NORMAL:
            raise exceptions.CDMError(f'Device has error on dispensing: {result[3]}')
        return result

    def get_configuration(self):
        LOG.debug('Get configuration')
        self.send(consts.COMMANDS.CONFIGURATION_STATUS)
        result = self.read()
        self.ack()
        return result

    def set_bill_thickness(self, cassete_num: int, count: int, margin: int):
        LOG.debug(f'Set bill thickness for cassete "{cassete_num}" "{count}" margin "{margin}"')
        self.send([consts.COMMANDS.SET_BILL_THICKNESS, cassete_num, count, margin])
        result = self.read()
        self.ack()
        return result

    def get_bill_thickness(self, cassete_num: int):
        LOG.debug(f'Get bill thickness for "{cassete_num}" cassete')
        self.send([consts.COMMANDS.GET_BILL_THICKNESS, cassete_num])
        result = self.read()
        self.ack()
        return result

    def set_bill_size(self, cassete_num: int, count: int, margin: int):
        LOG.debug(f'Set bill size for cassete "{cassete_num}" "{count}" margin "{margin}"')
        self.send([consts.COMMANDS.SET_BILL_SIZE, cassete_num, count, margin])
        result = self.read()
        self.ack()
        return result

    def get_bill_size(self, cassete_num: int):
        LOG.debug(f'Get bill size for "{cassete_num}" cassete')
        self.send([consts.COMMANDS.GET_BILL_SIZE, cassete_num])
        result = self.read()
        self.ack()
        return result

    def dispense_multi_cassete(self,
                               cassete0: int = 0,
                               cassete1: int = 0,
                               cassete2: int = 0,
                               cassete3: int = 0,
                               cassete4: int = 0,
                               cassete5: int = 0):
        LOG.debug(f'Dispense from multiple cassete: {cassete0} {cassete1} {cassete2} {cassete3} {cassete4} {cassete5}')
        self.send([consts.COMMANDS.MULTI_CASS_DISPENSE, cassete0, cassete1, cassete2, cassete3, cassete4, cassete5])
        result = self.read()
        self.ack()
        return result

    def get_reject_log(self):
        LOG.debug('Get reject log')
        self.send(consts.COMMANDS.REJECT_LOG)
        result = self.read()
        self.ack()
        return result

    def get_dispense_state(self):
        """
        0x30: Dispense end
        0x31: Dispense ready
        0x32: Dispensing
        """
        LOG.debug('Get dispense status')
        self.send(consts.COMMANDS.DISPENSE_STATE_CHECK)
        result = self.read()
        self.ack()
        return result

    def get_total_counts(self, count_type: int, count_state: int):
        """
        count_type - 0x30 pick up, 0x31 divert, 0x32 dispense
        count_state - 0x30 Read, 0xFF Clear
        """
        LOG.debug('Get total counts read and clear')
        self.send([consts.COMMANDS.TOTAL_COUNTS, count_type, count_state])
        result = self.read()
        self.ack()
        return result

    def sensor_read(self, cassete_num: int):
        LOG.debug(f'Get sensor read for "{cassete_num}"')
        self.send([consts.COMMANDS.SENSOR_READ, cassete_num])
        result = self.read()
        self.ack()
        return result
