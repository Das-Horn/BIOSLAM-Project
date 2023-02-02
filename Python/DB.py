from abc import ABC, abstractmethod


class DB(ABC):
    def __init__(self, username="", password="",address="localhost", port=0000, db_name=""):
        super.__init__()
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
    def __init__(self, username="", password="", address="localhost", port=0, db_name=""):
        super().__init__(username, password, address, port, db_name)