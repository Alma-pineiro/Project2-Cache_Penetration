import sys
import array
import csv
import math


def make_bit_array(bit_size, fill=0):

    #Calculates the amount of 32-bit integers that are needed
    int_size = (bit_size + 31) // 32

    if fill == 1:
        fill_value = 4294967296 # each array slot can store 4 bytes. 2^32 = 4294967296
        #All of the bits in the array will be set to 1

    else:
        fill_value = 0
        #All of the bits in the array will be set to 1

    #creates and returns the array 
    return array.array('I', [fill_value]*int_size)









