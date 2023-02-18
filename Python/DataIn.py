from abc import ABC, abstractmethod
import time
from DB import *
import wfdb
import serial

class DataFetcher(ABC):
    def __init__(self, DB=InfluxDB2(), length=60) -> None:
        # super().__init__()  
        self._buffer = []
        self._DB = DB
        self._buffer_length = length
        
    # GETTERS
    
    def get_buffer(self) -> tuple:
        return tuple(self._buffer)
    
    # SETTERS
    
    def set_buffer_length(self, length) -> None:
        if type(length) != int:
            raise TypeError("Value must be of type int representing seconds")
    
    # METHODS
    
    def update_buffer(self, val) -> None:
        """
        It takes a float, adds it to a list, then adds that list to a buffer
        
        :param val: The value to be added to the buffer
        """
        if type(val) != float:
            raise TypeError("Value must be of type float")
        time_of_in = int(round(time.time() * 1000000000))
        data_pack = [val, time_of_in]
        self._DB.write_data(data_pack)                            # Add new Data to the database
        self.clear_old_data()                                     # Clear any Data from the buffer past the time treshhold
        self._buffer.append(data_pack)                            # Append New Data pack to the buffer
        
    def clear_old_data(self) -> None:
        """
        It removes all the data from the buffer that is older than the time treshold. It breaks the loop if the time is not past the treshold
        """
        old_time = int(round((time.time() - self._buffer_length) * 1000000000))
        for i in range(0, len(self._buffer)):
            if self._buffer[0][1] <= old_time:
                self._buffer.pop(0)
            else:
                break
    
    def clear_buffer(self) -> None:
        self._buffer = []  
        
class Serial(DataFetcher):
    def __init__(self, DB=InfluxDB2(), length=60, port="COM11", baudrate=9600) -> None:
        super().__init__(DB, length)
        self.__serial_port = port
        self.__baudrate = baudrate
        self.__ser = serial.Serial()
        
        # Configure Serial Port Options
        self.__ser.port = self.__serial_port
        self.__ser.baudrate = self.__baudrate
        self.__ser.timeout = 1
    
    
    # Override update to accomadate the serial connection
    def update_buffer(self) -> None:
        """
        This function reads a line from the serial port, converts it to a voltage value, adds it to the
        database, clears any old data from the buffer, and adds the new data to the buffer
        """
        str_val = self.__ser.readline()
        
        val = int(str_val.split(" ")[2])
        val = float(val)/1023.0 * 5.0 # Convert from units to voltage at 10 bit resolution (default for arduino)
        
        time_of_in = int(round(time.time() * 1000000000))
        data_pack = [val, time_of_in]
        self._DB.write_data(data_pack)                            # Add new Data to the database
        self.clear_old_data()                                     # Clear any Data from the buffer past the time treshhold
        self._buffer.append(data_pack)    
    
        
class WFDB(DataFetcher):
    def __init__(self, DB=InfluxDB2(), length=60) -> None:
        super().__init__(DB, length)
        