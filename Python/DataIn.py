from abc import ABC, abstractmethod
import time
from DB import *
import wfdb
import serial
import paho.mqtt.client as mqtt
from threading import *
import sys
import struct
from scipy.signal import find_peaks

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
    
    def shutdown(self) -> None:
        pass
        
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
        
    # GETTERS
    
    def get_serial_port(self) -> str:
        return self.__serial_port
    
    def get_baudrate(self) -> int:
        return self.__baudrate
    
    
    # Override update to accomadate the serial connection
    def update_buffer(self) -> None:
        """
        This function reads a line from the serial port, converts it to a voltage value, adds it to the
        database, clears any old data from the buffer, and adds the new data to the buffer
        """
        if not self.__ser.is_open:
            self.__ser.open()    
        str_val = str(self.__ser.readline())
        try:
            print(str_val.split(" ")[2].replace("\\r\\n'", ''))
            val = int(str_val.split(" ")[2].replace("\\r\\n'", ''))
            val = float(val)/1023.0 * 5.0 # Convert from units to voltage at 10 bit resolution (default for arduino)
            print(f'Current Voltage = {val}')
            
            time_of_in = int(round(time.time() * 1000000000))
            data_pack = [val, time_of_in]
            self._DB.write_data(data_pack)                            # Add new Data to the database
            self.clear_old_data()                                     # Clear any Data from the buffer past the time treshhold
            self._buffer.append(data_pack)    
        except Exception as e:
            print("Error when reading from device")
            
class WFDB(DataFetcher):
    def __init__(self, DB=InfluxDB2(), length=60, file_path="") -> None:
        super().__init__(DB, length)
        # Check invalid file path
        if file_path == "":
            raise TypeError("Invalid File Path")
        
        self._record = wfdb.rdrecord(file_path)
        self._current_record = 0
    
    # GETTERS
    
    def get_record(self) -> object:
        """
        This method returns the record
        :return: The record object.
        """
        return self._record
    
    # SETTERS
    
    def set_record(self, file_path="") -> None:
        """
        This method takes in a file path and sets the record of the class to the record of
        the file path
        
        :param file_path: The path to the file you want to read
        """
        if file_path == "":
            raise TypeError("Invalid File Path")
        
        self._record = wfdb.rdrecord(file_path)
    
    # OVERRIDES
    
    def update_buffer(self) -> None:
        data_pack = [self._record.p_signal[self._current_record][0], int(round(time.time() * 1000000000))]
        print(f'Current Data : {data_pack[0]}\t\t Time : {data_pack[1]}')
        self._current_record += 1
        self._DB.write_data(data_pack)                            # Add new Data to the database
        self.clear_old_data()                                     # Clear any Data from the buffer past the time treshhold
        self._buffer.append(data_pack) 

class MQTT(DataFetcher):
    def __init__(self, DB=InfluxDB2(), length=60, server_name="localhost" ,username="", password="", topic="outTopic") -> None:
        super().__init__(DB, length)
        self.__server = server_name
        self.__username = username
        self.__password = password
        self.__topic = topic
        
        #MQTT Setup
        self.__client = mqtt.Client()
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        try:
            self.__client.connect(self.__server, 1883, 60) # Connect to the server
        except ConnectionRefusedError as ce:
            print("Error Broker refused to connect")
            sys.exit(0)
            
        
        self.__mqtt_update_thread = Thread(target=self.__client.loop_forever)
        self.__mqtt_update_thread.start()
        
    
    def on_message(self, client, userdata, msg) -> None:
        """
        It takes a message from the MQTT broker, and appends it to a buffer
        
        :param client: the client instance for this callback
        :param userdata: user data of any type and can be set when creating a new client instance or with
        user_data_set(userdata)
        :param msg: The message payload
        """
        time_of_in = int(round(time.time() * 1000000000))
        try:
            data_pack = [float(str(msg.payload.decode("UTF-8"))), time_of_in]
            self._buffer.append(data_pack)
            self._DB.write_data(data_pack)
        except ValueError as e:
            print("incorrect Value type recieved from MQTT")
        
    
    def on_connect(self, client, userdata, flags, rc) -> None:
        """
        The function is called when the client receives a CONNACK message from the broker in response to a
        connection request
        
        :param client: the client instance for this callback
        :param userdata: This is the user data of any type and can be set when creating a new client
        instance or with userdata_set(userdata)
        :param flags: response flags sent by the broker
        :param rc: the error code returned when connecting to the broker
        """
        print("Connection Established...")
        client.subscribe(self.__topic)
        
    def update_buffer(self) -> None:
        self.clear_old_data()
        
    def shutdown(self) -> None:
        self.__client.disconnect()