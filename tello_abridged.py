'''
TELLO_SIMPLE
    A module to help with controlling the Tello drones.
    Written by Roy Brushett while recovering from sugery.
'''
import socket

'''
DEFAULT_TELLO_COMMAND_IP - A constant representing the default IP address for commands on Tello per the documentation.
'''
DEFAULT_TELLO_COMMAND_IP = "192.168.10.1"

'''
DEFAULT_TELLO_COMMAND_PORT - A constant representing the default port for commands on Tello per the documentation.
'''
DEFAULT_TELLO_COMMAND_PORT = 8889

class Tello:
    '''
    A class for connecting to the Tello Drone and controlling it with commands.
    '''
    def __init__(self, ip=DEFAULT_TELLO_COMMAND_IP, port=DEFAULT_TELLO_COMMAND_PORT):
        '''
        Constructor for the class. You can set the default ip and port here if you've changed them.
        If not, call it with the blank constructor, for example:
        import tello_simple
        t = tello_simple.Tello()
        '''
        self.conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
        self.ip = ip
        self.port = port

    def connect(self, ip=None, port=None):
        '''
        Connects to the drone over wifi.

        Takes two optional parameters, the ip address of the drone, and the port of the drone.
        These can be left blank in most cases, it'd only change if you change the settings on the drone itself.
        
        Should not be called on it's own, use "connect_and_initialize" instead.
        '''
        ip = self.ip if ip is None else ip
        port = self.port if port is None else port
        self.conn.connect((ip,port))
           
    def disconnect(self):
        '''
        Ends the connection to the drone over wifi.
        Should be called at the end of your program or when you're othwerise finished sending commands.
        Returns nothing.
        '''
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()

    def connect_and_initialize(self, ip=None, port=None):
        '''
        Connects to the drone over wifi, and sends the initialization command to put it into command mode.
        This allows it to recieve other commands, and only has to be done once.

        This method returns the status message back from the drone (either an error or the string 'ok'), as well as the number of bytes sent.

        Takes two optional parameters, the ip address of the drone, and the port of the drone.
        These can be left blank in most cases, it'd only change if you change the settings on the drone itself.

        Example:
        import tello_simple
        t = tello_simple.Tello()
        t.connect_and_initialize()
        #returns: ('ok', 7)
        '''
        self.connect(ip, port)
        return self.initialize_command_mode()

    def initialize_command_mode(self):
        '''
        Sends the initialization command the the drone.
        Returns the response from the drone either the string 'ok' or an error.
        This method should not be used on it's own. Instead call "connect_and_initialize"
        '''
        return send_initalize_command_mode_command_to_socket(self.conn)

    def emergency(self):
        '''
        Sends the emergecny command to the drone, forcing it to kill power to the motors immediately.
        Returns the response from the drone ('ok', or an error), as well as the number of bytes send.
        
        For example:
            t.emergency()
            #returns: ('ok', 9)
        '''
        return send_emergency_command_to_socket(self.conn)

    def land(self):
        '''
        Sends a land command to the drone, instructing it to land.
        Returns the response from the drone ('ok', or an error), as well as the number of bytes send.
        
        For example:
            t.land()
            #returns: ('ok', 4)
        '''
        return send_land_command_to_socket(self.conn)

    def send_command(self,command_string):
        '''
        Sends a command string to the drone and returns it's response, as well as the number of bytes sent.
           command_string - A string representing a command, for example "takeoff"
           return - A tuple with two items:
            Item 1: Whatever was recieved from the drone
            Item 2: The number of bytes sent.
        For example:
            t.send_command("takeoff")
            #returns: ('ok', 7) 
        '''
        return send_command_to_socket(self.conn, command_string)

def send_command_to_socket(soc, command_string):
    '''
    This is a helper function that implements the behavior for a method in the Tello class.
    This should not be used on it's own, use the Tello class instead.
    Sends a command string to the drone and returns it's response, as well as the number of bytes sent.
       soc - A socket like object that represents the connection to tello.
       command_string - A string representing a command, for example "takeoff"
       return - ('ok' | error message, number_of_bytes)
    '''
    sent = soc.send(command_string.encode('utf-8'))
    return (soc.recv(1024).decode('utf-8'),sent)

LAND_COMMAND_STRING = "land"
def send_land_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    '''
    This is a helper function that implements the behavior for a method in the Tello class.
    This should not be used on it's own, use the Tello class instead.
    Sends the land command to the drone and returns it's response, as well as the number of bytes sent.
       soc - A socket like object that represents the connection to tello.
       send_command_to_socket (optional) - You can override the default send command if you'd like.
       return - ('ok' | error message, number_of_bytes)
    '''
    return send_command_to_socket(soc, LAND_COMMAND_STRING)

EMERGENCY_COMMAND_STRING = "emergency"
def send_emergency_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    '''
    This is a helper function that implements the behavior for a method in the Tello class.
    This should not be used on it's own, use the Tello class instead.
    Sends the emergecny command to the drone and returns it's response, as well as the number of bytes sent.
       soc - A socket like object that represents the connection to tello.
       send_command_to_socket (optional) - You can override the default send command if you'd like.
       return - ('ok' | error message, number_of_bytes)
    '''
    return send_command_to_socket(soc, EMERGENCY_COMMAND_STRING)

INITALIZE_COMMAND_COMMAND_STRING = "command"
def send_initalize_command_mode_command_to_socket(soc, send_command_to_socket=send_command_to_socket):
    '''
    This is a helper function that implements the behavior for a method in the Tello class.
    This should not be used on it's own, use the Tello class instead.
    Sends the initialization command to the drone and returns it's response, as well as the number of bytes sent.
       soc - A socket like object that represents the connection to tello.
       send_command_to_socket (optional) - You can override the default send command if you'd like.
       return - ('ok' | error message, number_of_bytes)
    '''
    return send_command_to_socket(soc, INITALIZE_COMMAND_COMMAND_STRING)
