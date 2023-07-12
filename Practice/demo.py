import os
import random
import time
import numpy as np
import pandas as pd
from practice03_28 import MyContainer

ALL_CAPS = 10

class SuperRaceCar:
    def __init__(self):
        self.current_speed = 0
        self.inside_temperature = 25
        self.__engine_manufacture = "AAA"
        self._max_speed = 300
    
    def speed_up(self):
        self.current_speed += 10
        self.inside_temperature += 1


def helper_function(input_data):
    result = 0
    # if len(input_data) == 0:
    if not input_data:
        return False
    for ele in input_data:
        if ele == ALL_CAPS:
            print("Find !!")
            result = 1
        else:
            print("Not Find")
    return True if result == 1 else False

data = [1,2,3,4,5]
r = helper_function(data)