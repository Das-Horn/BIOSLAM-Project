from abc import ABC, abstractmethod
import time
from DB import *

class DataFetcher(ABC):
    def __init__(self, DB=InfluxDB2()) -> None:
        super().__init__()  
        self._buffer = []
        self._DB = DB
        
    # GETTERS
    
    def get_buffer(self) -> list:
        return self._buffer
    
    # METHODS
    
    def update_buffer(self, val) -> None:
        if type(val) != float:
            raise TypeError("Value must be of type float")
        time_of_in = int(round(time.time() * 1000000000))
        data_pack = [val, time_of_in]
        DB.write_data(data_pack)
        
        
        
        
class Serial(DataFetcher):
    def __init__(self, DB=InfluxDB2()) -> None:
        super().__init__(DB)
        
class WFDB(DataFetcher):
    def __init__(self) -> None:
        super().__init__()