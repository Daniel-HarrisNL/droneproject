import socket
import enum


class FlipDirection(enum.Enum):
    LEFT = 'l'
    RIGHT = 'r'
    FORWARD = 'f'
    BACK = 'b'


DEFAULT_TELLO_COMMAND_IP = "192.168.10.1"
DEFAULT_TELLO_COMMAND_PORT = 8889


class Tello:
    def __init__(self, ip=DEFAULT_TELLO_COMMAND_IP, port=DEFAULT_TELLO_COMMAND_PORT):
        self.conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port

    def connect(self, ip=None, port=None):
        ip = self.ip if ip is None else ip
        port = self.port if port is None else port
        self.conn.connect((ip, port))

    def disconnect(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()

    def connect_and_initialize(self, ip=None, port=None):
        self.connect(ip, port)
        self.initialize_command_mode()

    def initialize_command_mode(self):
        return send_initalize_command_mode_command_to_socket(self.conn)

    def fly_up(self, cm):
        return send_fly_up_command_to_socket(self.conn, cm)

    def fly_down(self, cm):
        return send_fly_down_command_to_socket(self.conn, cm)

    def fly_left(self, cm):
        return send_fly_left_command_to_socket(self.conn, cm)

    def fly_right(self, cm):
        return send_fly_right_command_to_socket(self.conn, cm)

    def fly_forward(self, cm):
        return send_fly_forward_command_to_socket(self.conn, cm)

    def fly_backward(self, cm):
        return send_fly_backward_command_to_socket(self.conn, cm)

    def rotate_clockwise(self, degrees):
        return send_rotate_clockwise_command_to_socket(self.conn, degrees)

    def rotate_counterclockwise(self, degrees):
        return send_rotate_counterclockwise_command_to_socket(self.conn, degrees)

    def takeoff(self):
        return send_takeoff_command_to_socket(self.conn)

    def land(self):
        return send_land_command_to_socket(self.conn)

    def emergency(self):
        return send_emergency_command_to_socket(self.conn)

    def stop(self):
        return send_stop_command_to_socket(self.conn)

    def flip(self, direction):
        return send_flip_command_to_socket(self.conn, direction)

    def set_speed(self, speed):
        return send_set_speed_command_to_socket(self.conn, speed)

    # def turn_stream_off(self):
    #    return send_turn_strem_off_command_to_socket(self.conn, degrees)

    # def turn_stream_on(self):
    #    return send_turn_strem_off_command_to_socket(self.conn, degrees)

    def send_command(self, command_string):
        return send_command_to_socket(self.conn, command_string)


## SOCKET SEND HELPER ##

def send_command_to_socket(soc, command_string):
    sent = soc.send(command_string.encode('utf-8'))
    return (soc.recv(1024).decode('utf-8'), sent)


## FLY COMMANDS AND CONSTANTS ##

CM_OUT_OF_RANGE_VALUE_ERROR_TEXT = "The number of centemeters to fly must be a number between 20 and 500 inclusive."
CM_OUT_OF_RANGE_VALUE_ERROR = ValueError(CM_OUT_OF_RANGE_VALUE_ERROR_TEXT)


def fly_cm_in_bounds(cm):
    return (cm >= 20) and (cm <= 500)


UP_COMMAND_FORMAT_STRING = 'up {0}'


def send_fly_up_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                  cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, UP_COMMAND_FORMAT_STRING.format(cm))


DOWN_COMMAND_FORMAT_STRING = 'down {0}'


def send_fly_down_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                    cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, DOWN_COMMAND_FORMAT_STRING.format(cm))


LEFT_COMMAND_FORMAT_STRING = 'left {0}'


def send_fly_left_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                    cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, LEFT_COMMAND_FORMAT_STRING.format(cm))


RIGHT_COMMAND_FORMAT_STRING = 'right {0}'


def send_fly_right_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                     cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, RIGHT_COMMAND_FORMAT_STRING.format(cm))


FORWARD_COMMAND_FORMAT_STRING = 'forward {0}'


def send_fly_forward_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                       cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, FORWARD_COMMAND_FORMAT_STRING.format(cm))


BACKWARD_COMMAND_FORMAT_STRING = 'back {0}'


def send_fly_backward_command_to_socket(soc, cm, send_command_to_socket=send_command_to_socket,
                                        cm_out_of_range_error=CM_OUT_OF_RANGE_VALUE_ERROR):
    if not fly_cm_in_bounds(cm):
        raise cm_out_of_range_error
    return send_command_to_socket(soc, BACKWARD_COMMAND_FORMAT_STRING.format(cm))


## ROTATE COMMANDS AND CONSTANTS ##

ROTATE_DEGREES_OUT_OF_RANGE_VALUE_ERROR_TEXT = "The number of degrees to rotate must be between 1 and 360."
ROTATE_DEGREES_OUT_OF_RANGE_VALUE_ERROR = ValueError(ROTATE_DEGREES_OUT_OF_RANGE_VALUE_ERROR_TEXT)


def rotate_degrees_in_bounds(degrees):
    return (degrees >= 1) or (degrees <= 360)


ROTATE_CLOCKWISE_COMMAND_FORMAT_STRING = 'cw {0}'


def send_rotate_clockwise_command_to_socket(soc, degrees, send_command_to_socket=send_command_to_socket,
                                            rotate_degrees_out_of_range_error=ROTATE_DEGREES_OUT_OF_RANGE_VALUE_ERROR):
    if not rotate_degrees_in_bounds(degrees):
        raise rotate_degrees_out_of_range_error
    return send_command_to_socket(soc, ROTATE_CLOCKWISE_COMMAND_FORMAT_STRING.format(degrees))


ROTATE_COUNTERCLOCKWISE_COMMAND_FORMAT_STRING = 'ccw {0}'


def send_rotate_counterclockwise_command_to_socket(soc, degrees, send_command_to_socket=send_command_to_socket,
                                                   rotate_degrees_out_of_range_error=ROTATE_DEGREES_OUT_OF_RANGE_VALUE_ERROR):
    if not rotate_degrees_in_bounds(degrees):
        raise rotate_degrees_out_of_range_error
    return send_command_to_socket(soc, ROTATE_COUNTERCLOCKWISE_COMMAND_FORMAT_STRING.format(degrees))


## SET SPEED COMMAND AND CONSTANTS ##

INVALID_SPEED_VALUE_ERROR = ValueError("The speed for the set speed command must be between 10cm/s and 100cm/s.")


def valid_set_speed(speed):
    return (speed >= 10) and (speed <= 100)


SPEED_COMMAND_FORMAT_STRING = "speed {0}"


def send_set_speed_command_to_socket(soc, speed_cm_per_second, send_command_to_socket=send_command_to_socket,
                                     invalid_speed_error=INVALID_SPEED_VALUE_ERROR):
    if not valid_set_speed(speed_cm_per_second):
        raise invalid_speed_error
    return send_command_to_socket(soc, SPEED_COMMAND_FORMAT_STRING.format(speed_cm_per_second))


## FLIP COMMAND AND CONSTANTS ##

FLIP_INVALID_DIRECTION_VALUE_ERROR = ValueError(
    "Invalid direction specified for flip. Must be either a string 'l', 'r', 'f', 'b', or FlipDirection.LEFT, FlipDirection.RIGHT, FlipDirection.FORWARD, FlipDirection.BACK from the FlipDirection Enum.")
FLIP_DIRECTION_LEFT_STRING = 'l'
FLIP_DIRECTION_RIGHT_STRING = 'r'
FLIP_DIRECTION_FORWARD_STRING = 'f'
FLIP_DIRECTION_BACK_STRING = 'b'


def valid_direction(direction):
    return direction in [FLIP_DIRECTION_LEFT_STRING, FLIP_DIRECTION_RIGHT_STRING, FLIP_DIRECTION_FORWARD_STRING,
                         FLIP_DIRECTION_BACK_STRING, FlipDirection.LEFT, FlipDirection.RIGHT, FlipDirection.FORWARD,
                         FlipDirection.BACK]


def get_direction_as_string(direction, invalid_direction_error=FLIP_INVALID_DIRECTION_VALUE_ERROR):
    if direction == FlipDirection.LEFT or direction == FLIP_DIRECTION_LEFT_STRING:
        return FLIP_DIRECTION_LEFT_STRING
    elif direction == FlipDirection.RIGHT or direction == FLIP_DIRECTION_RIGHT_STRING:
        return FLIP_DIRECTION_RIGHT_STRING
    elif direction == FlipDirection.FORWARD or direction == FLIP_DIRECTION_FORWARD_STRING:
        return FLIP_DIRECTION_FORWARD_STRING
    elif direction == FlipDirection.BACK or direction == FLIP_DIRECTION_BACK_STRING:
        return FLIP_DIRECTION_BACK_STRING
    else:
        raise invalid_direction_error


FLIP_COMMAND_FORMAT_STRING = "flip {0}"


def send_flip_command_to_socket(soc, direction, send_command_to_socket=send_command_to_socket,
                                invalid_direction_error=FLIP_INVALID_DIRECTION_VALUE_ERROR):
    if not valid_direction(direction):
        raise invalid_direction_error
    s_dir = get_direction_as_string(direction)
    return send_command_to_socket(soc, FLIP_COMMAND_FORMAT_STRING.format(s_dir))


## PARAMETERLESS COMMANDS AND CONSTANTS ##

TAKEOFF_COMMAND_STRING = "takeoff"


def send_takeoff_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, TAKEOFF_COMMAND_STRING)


LAND_COMMAND_STRING = "land"


def send_land_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, LAND_COMMAND_STRING)


STREAMOFF_COMMAND_STRING = "streamoff"


def send_turn_stream_off_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, STREAMOFF_COMMAND_STRING)


STREAMON_COMMAND_STRING = "streamon"


def send_turn_stream_on_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, STREAMON_COMMAND_STRING)


INITALIZE_COMMAND_COMMAND_STRING = "command"


def send_initalize_command_mode_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, INITALIZE_COMMAND_COMMAND_STRING)


STOP_COMMAND_STRING = "stop"


def send_stop_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, )


EMERGENCY_COMMAND_STRING = "emergency"


def send_emergency_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    return send_command_to_socket(soc, EMERGENCY_COMMAND_STRING)
