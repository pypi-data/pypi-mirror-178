import numpy as np 
import h5py 
import os 
import re 

class FrequencyJump:
    """
    
    change frequency smoothly with explicitly defined step frequency limit 
    
    freq_start = current frequency
    freq_stop = target frequency
    freq_step  = maximum step allowed 
    
    """
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def find_freq_start(self):
        freq = [value for key,value in self.kwargs.items() 
                             if re.search('(start)|(initial)|(begin)',key, re.IGNORECASE)][0]
        return freq
        
    def find_freq_stop(self):
        freq = [value for key,value in self.kwargs.items() 
                             if re.search('(stop)|(final)|(end)',key, re.IGNORECASE)][0]
        return freq
        
    def find_freq_step_max(self):
        freq = [value for key,value in self.kwargs.items() 
                             if re.search('(step)',key, re.IGNORECASE)][0]
        return freq
    
    def decimal_place(self):
        """
        how many decimal place used, default 6 
        
        """
        try:
            n = [value for key,value in self.kwargs.items() 
                             if re.search('(decimal)|(digit)|(accuracy)',key, re.IGNORECASE)][0]
        except:
            n = 6
            
        return round(n)
        
    def freq_list(self):
        self.freq_start = self.find_freq_start()
        self.freq_stop = self.find_freq_stop()
        self.freq_step_max = self.find_freq_step_max()
        freq_range = abs(self.freq_stop - self.freq_start)
        n_step = int(np.floor(freq_range / self.freq_step_max) + 2)
        f_list = np.linspace(self.freq_start, self.freq_stop, n_step)
        
        return np.round(f_list, self.decimal_place())
        