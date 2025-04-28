import sys
import array
import csv
import math


def make_bit_array(bit_size, fill=0):
    """"
    Creates a bit array, represented by an array of unsigned 32-bit integers. 
    
    Parameters: 
        bit_size (int): Size of the bit array in bits.
        fill (int): The initial value of the bits. Defaults to 0. 
    
        Returns: 
            An array where all of its bits are set to 0. 
    """

    #Calculates the amount of 32-bit integers that are needed
    int_size = (bit_size + 31) // 32

    if fill == 1:
        fill_value = 0xFFFFFFFF # each array slot can store 4 bytes. 2^32 = 4294967296 or 0xFFFFFFFF in hexadecimal form
        #All of the bits in the array will be set to 1

    else:
        fill_value = 0
        #All of the bits in the array will be set to 1

    #creates and returns the array 
    return array.array('I', [fill_value]*int_size)


def test_Bit(array_name, bit_num):
    """"
    Checks if the specific bit in the array is set to 1. 

    Parameters: 
        array_name (array.array): The bit array.
        bit_num (int): The position of the bit that we want to verify.
    
    Returns: 
        int: A non-zero value if the bit is set to 1; otherwise, 0.
    """

    #calculates in which 32-bit block the bit is in
    bit_index = bit_num // 32 

    #calculates the bits position from (index 0 - index 31)
    bit_pos = bit_num % 32

    mask = 1 << bit_pos

    final_array = array_name[bit_index] & mask 
    return final_array

#sets  the bit in the specified position in the bit to 1
def set_Bit(array_name, bit_num):
    """
    Sets the bit in the specified position in the bit to 1. 

    Parameters:
        array_name (array.array): The bit array.
        bit_num (int): The position of the bit that we want to verify.
    
        Returns: 
            array_name (array.array): The array with the correct bits set to 1.

    """
    #determines which element in the array to use 
    index = bit_num // 32       

    #calculates the position of the bit within that 32-bit integer
    offset = bit_num % 32  

    #creates a bitmask with a 1 at the correct position 
    mask = 1 << offset   

    #sets bit at the target position to 1 
    array_name[index] |= mask   
 
    return array_name[index] 


def calculate_hash(data, bitArraySize, k):
    """
    Generates a hash function for the selected data. 

    Parameters: 
        data (str): The email to hash
        bitArraySize (int): Size of the array. 
        k (int): Index value to vary the hash 

    Returns: 
        int: A hash value that can be found in range. 
    """
    return hash(f"{data}{k}") % bitArraySize

def Bloom_Filter(n,p):
    """
    Calculates the amount of functions that are needed for the Bloom Filter.

    Parameters: 
        n (int): Number of items that will be in Bloom Filter.
        p (float): Probability of false positives, fraction between 0 and 1 or a number indicating 1-in-p.
    
    Returns: 
        m (int): Number of bits in the filter.
        k (int): Number of hash functions.
    """
    m = math.ceil((n*math.log(p)) / math.log(1/pow(2, math.log(2))))
    k =  round((m/n)*math.log(2))

    return m,k
def Bloom_Filter_adder(bitArray, data, bitArraySize,k):
    """
    Adds data to the bloom filter.

    Parameters: 
        bitArray(array.array): Bit array that represents the Bloom Filter.
        data (str): The email that will be added to the Bloom Filter.
        bitArraySize (int): The size of the bit array.
        k (int): Number of hash functions needed.
    """
    for hash_round in range(k):
        bit_index = calculate_hash(data, bitArraySize, hash_round)
        set_Bit(bitArray, bit_index)

def verifyBloomFilter(email, bitArray, bitArraySize, k):
    """
    Verifies if the element is probably in the Bloom Filter.

    Parameters: 
        email (str): The email to check. 
        bitArray (array.array): Bit array that represents the Bloom Filter.
        bitArraySize (int): The size of the bit array.
        k (int):  k (int): Number of hash functions needed.
    Returns:
        "Probably in teh DB": if the email is might be in the filter.
        "Not in the DB": if the eail is not in the filter. 
    """
    for i in range(k):
        index_to_verify = calculate_hash(email, bitArraySize, i)
        if test_Bit(bitArray, index_to_verify) == 0:
            print(f"{email},Not in the DB")
            return
    print(f"{email},Probably in the DB")

def email_Reader(filename):
    """
    Reads emails from the csv file. 

    Parameters: 
        filename (str): Name of the csv file that contains all of the emails. 
    
    Returns: 
        emails (list): A list that contains all of the emails from the csv file. 
    """
     
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        emails = []

        for row in reader:
            for email in row:
                emails.append(email)
        return emails
     
if len(sys.argv) > 1:
    file1 = sys.argv[1]  
    file2 = sys.argv[2]

    emails = email_Reader(file1)
    m, k = Bloom_Filter(len(emails), 0.0000001)

    b_array = make_bit_array(m)

    for e in emails:
        Bloom_Filter_adder(b_array, e, m, k) #Adds emails to the Bloom Filter 

    compare_emails  = email_Reader(file2)

    for e in compare_emails:
        verifyBloomFilter(e, b_array, m, k) #Verifies if the emails are in the Bloom Filter. 


