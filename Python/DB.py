from abc import ABC, abstractmethod
from influxdb_client import InfluxDBClient
import asyncio


class DB(ABC):
    def __init__(self, username="", password="",address="localhost", port=0000, db_name=""):
        # super.__init__()
        self._username = username
        self._password = password
        self._address = address
        self._port = port
        self._database_name = db_name
    
    #   GETTERS
    
    def get_username(self) -> str:
        return self._username
    
    def get_password(self) -> str:
        return self._password
    
    def get_address(self) -> str:
        return self._address
    
    def get_port(self) -> int:
        return self._port
    
    def get_database_name(self) -> str:
        return self._database_name
    
    #   SETTERS
    
    def set_username(self, username) -> None:
        if type(username) != str:
            raise TypeError("User name must be of type string")
        self._username = username
        
    def set_password(self, password) -> None:
        if type(password) != str:
            raise TypeError("Password must be of type string")
        self._password = password
        
    def set_address(self, address) -> None:
        if type(address) != str:
            raise TypeError("Address must be of type string")
        self._address = address
    
    def set_port(self, port) -> None:
        if type(port) != int:
            raise TypeError("Port must be of type integer")
        self._port = port
        
    def set_database_name(self, db_name) -> None:
        if type(db_name) != str:
            raise TypeError("Database name must be of type int")
        self._database_name = db_name
    
    #   METHODS
    
    def write_data(self, data) -> None:
        """Overwritten in child classes
        """
        pass
    
    def read_data(self) -> tuple:
        """Overwritten in child classes
        """
        pass
    
    #   OVERRIDES
    
    def __str__(self) -> str:
        return f'{self._database_name}:\nusername:\t{self._username}\naddress:\t{self._address}:{self._port}\n'
    
class InfluxDB2(DB):
    def __init__(self, token="", address="localhost", port=8086, db_name="", org=""):
        super().__init__("", "", address, port, db_name)
        self._org = org
        self._token = token
        # Create Client & api for Influx
        self._client = InfluxDBClient(url=f'http://{self._address}:{self._port}', token=self._token, org=self._org)
        self._write_api = self._client.write_api()
        
    def write_data(self, data, record="REALTIME", unit="mV", measurement="EOG") -> None:
        """
        It takes in a list of two values, the first being the value of the data point and the second being
        the time of the data point. It then creates a dictionary with the appropriate tags and fields and
        writes it to the database
        
        :param data: The data to be written to the database. This must be in the format of a list with 2
        values. The first value is the data point, and the second value is the timestamp
        :param record: The name of the record, defaults to REEALTIME (optional)
        :param unit: The unit of the data, defaults to mV (optional)
        :param measurement: The name of the measurement, defaults to EOG (optional)
        """
        if type(data) != list or len(data) != 2:
            raise TypeError("Data must be in list format with 2 values")
        
        point = {
                "measurement": measurement,
                "tags": {
                    "Record":record,
                    "Unit": unit,
                    "Measurement":measurement
                },
                "fields": {
                    "value":data[0]
                },
                "time": data[1]
            }
        
        self._write_api.write(self._database_name, self._org, point)
        # print("Write TO DB")