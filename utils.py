import os 
from pathlib import Path 

    
class Month(object):
    def __init__(self, nr=1):
        self._create_month_mapping()
        self.nr = nr
        
    def __str__(self): 
        return self._num_to_str.get(self.nr).capitalize()
        
    def __repr__(self): 
        return f'class: Month({self.nr})' 
        
    @property
    def month(self):
        return self.__nr 
    
    @month.setter
    def month(self, n): 
        if type(n) == int:
            if n < 1 or n > 12:
                raise ValueError('Out of range. Month must be between 1 and 12') 
            self.__nr = n 
        elif type(n) == str:
            nr = self._str_to_num.get(n.lower())
            if not nr:
                raise ValueError(f'{n} is not a valid month!') 
            self.__nr = nr 

    @property
    def number(self):
        return self.nr

    @property
    def str(self):
        return self._num_to_str.get(self.nr).capitalize()

    def next(self, inplace=False): 
        next_nr = self.nr + 1
        if next_nr == 13: 
            next_nr = 1 
        if inplace:
            self.__nr = next_nr
        else:
            return Month(next_nr)

    def previous(self, inplace=False): 
        previous_nr = self.nr - 1
        if previous_nr == 0: 
            previous_nr = 12 
        if inplace:
            self.__nr = previous_nr
        else:
            return Month(previous_nr)

    def _create_month_mapping(self):
        self._num_list = list(range(1, 13))
        self._str_list = ['januari', 
                            'februari', 
                            'mars', 
                            'april', 
                            'maj', 
                            'juni', 
                            'juli', 
                            'augusti', 
                            'september',  
                            'oktober',  
                            'november', 
                            'december']
        self._num_to_str = {}
        
        self._str_to_num = dict(zip(self._str_list, self._num_list))
        self._num_to_str = dict(zip(self._num_list, self._str_list))
       

