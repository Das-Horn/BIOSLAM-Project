from abc import ABC, abstractmethod
import time
from DB import *

class DataFetcher(ABC):
    def __init__(self, DB=InfluxDB2(), length=60) -> None:
        super().__init__()  
        self._buffer = []
        self._DB = DB
        self._buffer_length = length
        
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
        clear_old_data()
        
    def clear_old_data(self) -> None:
        old_time = int(round((time.time() - self._buffer_length) * 1000000000))
        for i in range(0, len(self._buffer)):
            if self._buffer[0][1] <= old_time:
                self._buffer.pop(i)
        
        
        
        
class Serial(DataFetcher):
    def __init__(self, DB=InfluxDB2()) -> None:
        super().__init__(DB)
        
class WFDB(DataFetcher):
    def __init__(self) -> None:
        super().__init__()