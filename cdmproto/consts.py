class COMMANDS:
    # system
    ACK = 0x06
    STX = 0x02
    ETX = 0x03
    # all commands
    INITIALIZE = 0x30
    READ_STATUS = 0x31
    DIAGNOSTIC = 0x32
    DISPENSE_BILL = 0x33
    LAST_STATUS = 0x34
    CONFIGURATION_STATUS = 0x35
    SET_BILL_THICKNESS = 0x36
    GET_BILL_THICKNESS = 0x37
    SEET_BILL_SIZE = 0x38
    GET_BILL_SIZE = 0x39
    MULTI_CASS_DISPENSE = 0x3a
    LEARN_BILL_PARAMETER = 0x40
    CSS_STATUS_CHECK = 0x41
    CHANGED_CASS_BOX = 0x42
    REJECT_LOG = 0x43
    SENSOR_READ = 0x44
    DISPENSE_STATE_CHECK = 0x45
    TOTAL_COUNTS = 0x46


class ERROR_CODES:
    NORMAL = 0x30  # normal
    SRAM_ERROR = 0x31  # Static memory error
    DIVERTER_SOLENOID_ERROR = 0x32  # Steering solenoid error
    SENSOR_ERROR = 0x33  # Sensor error
    DIVERTER_SWITCH_ERROR = 0x34  # Steering switch error
    ENCODER_MOTOR_ERROR = 0x35  # Encoder, motor error

    LOADING_JAM_0 = 0x36  # (At Left, Right, Center sensors) Coins (Cash Box 1)
    LOADING_JAM_1 = 0x37
    LOADING_JAM_2 = 0x38
    LOADING_JAM_3 = 0x39
    LOADING_JAM_4 = 0x3a
    LOADING_JAM_5 = 0x3b

    MIDDLE_JAM_0 = 0x3c  # Cards at Middle sensor (cassette 1)
    MIDDLE_JAM_1 = 0x3d
    MIDDLE_JAM_2 = 0x3e
    MIDDLE_JAM_3 = 0x3f
    MIDDLE_JAM_4 = 0x40
    MIDDLE_JAM_5 = 0x41

    THICK_REF_JAM = 0x42  # Cards at the thickness sensor
    EXIT_JAM = 0x43  # Card currency

    REJECT_ERROR_5_TIMES = 0x44  # 5 consecutive chargebacks
    PICK_UP_SOLENOID_ERROR = 0x45  # Pick up solenoid error
    INITIAL_THICK_VALUE_ERROR = 0x46  # Wrong initial thickness value
    NO_FEED = 0x47  # No coins (near near end)

    CASS_COMM_ERROR1 = 0x48  # Communication between PC and CDM is abnormal
    CASS_COMM_ERROR2 = 0x49  # Communication between CDM main board and cash box circuit board is abnormal
    CAS_NONE_EXIST = 0x4a  # No such cash box
    BILL_CLASS_ERROR = 0x4b  # Wrong cassette placement or BILL_CLASS sensor error
    EEP_FAIL = 0x4c  # EEPROM Fail
    MOTOR_CPU_FAIL = 0x4d  # Motor CPU error
    BILL_CNT_ERROR = 0x4e  # Coin count incorrect
    SENSOR_DETECT_ERROR = 0x4f  # Sensor detection error
    SHUTDOWN_ERROR = 0x50  # Blackout process
    DIV_GATE_JAM = 0x51  # Cards at Turning Doors

    PICK_UP_SOLENOID_ERROR_2 = 0x52  # Pick up solenoid error 2-cassette 2
    PICK_UP_SOLENOID_ERROR_3 = 0x53
    PICK_UP_SOLENOID_ERROR_4 = 0x54
    PICK_UP_SOLENOID_ERROR_5 = 0x55
    PICK_UP_SOLENOID_ERROR_6 = 0x56

    ILLEGAL_BILL = 0x57  # Illegal banknote parameters

    BILL_CLASS_ERROR_1 = 0x58  # Cassette 1 incorrectly placed or BILL_CLASS sensor incorrect
    BILL_CLASS_ERROR_2 = 0x59
    BILL_CLASS_ERROR_3 = 0x5a
    BILL_CLASS_ERROR_4 = 0x5b
    BILL_CLASS_ERROR_5 = 0x5c
    BILL_CLASS_ERROR_6 = 0x5d

    CASSETE_BOX_NO_1 = 0x5e  # Cashless Box 1
    CASSETE_BOX_NO_2 = 0x5f
    CASSETE_BOX_NO_3 = 0x60
    CASSETE_BOX_NO_4 = 0x61
    CASSETE_BOX_NO_5 = 0x62
    CASSETE_BOX_NO_6 = 0x63

    CASSETE_BOX_EMPTY_1 = 0x64  # Cash box 1 empty
    CASSETE_BOX_EMPTY_2 = 0x65
    CASSETE_BOX_EMPTY_3 = 0x66
    CASSETE_BOX_EMPTY_4 = 0x67
    CASSETE_BOX_EMPTY_5 = 0x68
    CASSETE_BOX_EMPTY_6 = 0x69


class REJECT_CODES:
    NO_REJECT = 0x00  # No chargeback
    LENGTH_LONG = 0x01  # Banknotes are too long
    DOUBLE = 0x02  # Paper money is too thick (may be two)
    SKEW = 0x04  # Banknote tilt
    NEAR = 0x08  # The two notes before and after are too close
    MORE = 0x10  # More coins
    RESERVE = 0x20  # Reserve
    LENGTH_SHORT = 0x40  # Notes are too short
    WIDTH = 0x80  # Notes are too wide
