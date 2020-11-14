'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Drone Project

Authors: Blake Legge, Lyndon Loveys, Nicholas Hodder, Annette Clarke, Daniel Harris
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Imports
import tello_abridged as ta

# Functions
'''
DEFAULT_TELLO_COMMAND_IP - A constant representing the default IP address for commands on Tello per the documentation.
'''
DEFAULT_TELLO_COMMAND_IP = "192.168.10.1"

'''
DEFAULT_TELLO_COMMAND_PORT - A constant representing the default port for commands on Tello per the documentation.
'''
DEFAULT_TELLO_COMMAND_PORT = 8889

t = ta.Tello()

# Program start
if __name__ == "__main__":
    print("Program starts here")
    # t.connect_and_initialize()
    import gui
    t.disconnect()
