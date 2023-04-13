from abc import ABC, abstractmethod
import pyautogui
from DataIn import *
import matplotlib.pyplot as plot
import numpy as np


class Controller(ABC):
    def __init__(self, data_fetcher=Serial(), upper_tresh=1, lower_tresh=-1, baseline=0) -> None:
        # super().__init__()
        self._data_fetcher = data_fetcher
        self._upper_treshold = upper_tresh
        self._lower_treshold = lower_tresh
        self._baseline = baseline
        self._current_stats = [0, 0]
    
    # GETTERS
    
    def get_upper_treshold(self) -> int:
        return self._upper_treshold
    
    def get_lower_treshold(self) -> int:
        return self._lower_treshold
    
    def get_baseline(self) -> int:
        return self._baseline
    
    def get_current_stats(self) -> tuple:
        return tuple(self._current_stats)
    
    # SETTERS
    
    def set_upper_treshold(self, upper_treshold=1) -> None:
        """
        Takes in a parameter upper_treshold of type int or float and
        sets the value of  _upper_treshold
        
        :param upper_treshold: The upper treshold, defaults to 1 (optional)
        """
        if type(upper_treshold) != int or type(upper_treshold) != float:
            raise TypeError("Upper Threshold must be of type int or float")
        self._upper_treshold = upper_treshold
    
    def set_lower_treshold(self, lower_treshold=-1) -> None:
        """
        Takes in a parameter lower_treshold of type int or float and
        sets _lower_treshold
        
        :param lower_treshold: The lower threshold, defaults to -1 (optional)
        """
        if type(lower_treshold) != int or type(lower_treshold) != float:
            raise TypeError("Lower Threshold must be of type int or float")
        self._lower_treshold = lower_treshold
    
    def set_baseline(self, baseline=0) -> None:
        """
        Takes in a parameter baseline of type int or float and
        sets _baseline
        
        :param baseline: The baseline value, defaults to 0 (optional)
        """
        if type(baseline) != int or type(baseline) != float:
            raise TypeError("Baseline must be of type int or float")
        self._baseline = baseline
    
    #   METHOD USED FOR CHECKING BUFFER AND MAKING ACTIONS - OVERWRITE THIS
    def update(self) -> tuple:
        """
        It takes a list of numbers, and counts how many times the numbers go above a certain threshold, and
        how many times they go below a certain threshold
        :return: A tuple of the current stats.
        """
        
        buffer = self._data_fetcher.get_buffer()
        upper_bool = lower_bool = False
        
        for i in buffer:
            if i >= self._upper_treshold and not upper_bool:
                self._current_stats[0] += 1
                upper_bool = True
            elif i <= self._lower_treshold and not lower_bool:
                self._current_stats[1] += 1
                lower_bool = True
            elif i < self._upper_treshold and i > self._lower_treshold:
                lower_bool = False
                upper_bool = False
            
        return tuple(self._current_stats)
    
class PCInputs(Controller):
    def __init__(self, data_fetcher=Serial(), upper_tresh=1, lower_tresh=-1, baseline=0, mode="Relative") -> None:
        super().__init__(data_fetcher, upper_tresh, lower_tresh, baseline)
        self._mode = mode
    
    def update(self) -> tuple:
        self._data_fetcher.update_buffer()
        
        buffer = self._data_fetcher.get_buffer()
        #upper_bool = lower_bool = False
        try :                                                                               # ERROR HANDLE : Empty buffer
            if buffer[0][0] >= self._upper_treshold and not upper_bool:
                self._current_stats[0] += 1
                # pyautogui.scroll(10)
                upper_bool = True
            elif buffer[0][0] <= self._lower_treshold and not lower_bool:
                self._current_stats[1] += 1
                # pyautogui.scroll(-10)
                lower_bool = True
            elif buffer[0][0] <= self._upper_treshold and buffer[0][0] >= self._lower_treshold:
                lower_bool = False
                upper_bool = False
        except IndexError as ie:
            print("Buffer is currently empty")
            print(buffer)

class HeartRate(Controller):
    def __init__(self, data_fetcher=Serial(), upper_tresh=1, lower_tresh=-1, baseline=0) -> None:
        super().__init__(data_fetcher, upper_tresh, lower_tresh, baseline)
    
    
    def update(self) -> tuple:
        self._data_fetcher.update_buffer()
        data_array = np.array([])
        for i in self._data_fetcher.get_buffer():
            data_array = np.append(data_array, i[0])
        
        peaks, _= find_peaks(data_array,prominence=1, distance=80)
        # try:
        plot.clf()
        plot.plot(data_array, color="blue")
        plot.plot(peaks, data_array[peaks], "xr")
        plot.title(f'{len(peaks) * 4} bpm')
        plot.pause(0.001)
        # except ValueError as e:
        #     plot.clf()
        #     plot.plot(time_array, data_array, color="blue")
        #     plot.pause(0.001)
        
        return len(peaks)
    