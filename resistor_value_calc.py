'''
Documentation, License etc.

@package resistor_value_calc
'''
from numba import autojit, prange
import urllib.request
import csv 
import operator
from io import StringIO
import re
from collections import OrderedDict


INPUT_VOLTAGE = 3.3
MAX_DAC = 255 

REG_REF_VOLTAGE = .8
MAX_REG_VOLTAGE = 1.8
MIN_REG_VOLTAGE = 0

RESISTOR_MIN = 20000
RESISTOR_MAX = 100000
RESISTOR_JUMP = 100

R1_MIN = RESISTOR_MIN
R1_MAX = RESISTOR_MAX

R2_MIN = RESISTOR_MIN
R2_MAX = RESISTOR_MAX

R3_MIN = RESISTOR_MIN
R3_MAX = RESISTOR_MAX


DACV_LOW = INPUT_VOLTAGE*0/MAX_DAC
DACV_HIGH = INPUT_VOLTAGE*MAX_DAC/MAX_DAC
MAX_VOLT_DEV = .01



def convert(value):
    if value:
        # determine multiplier
        multiplier = 1
        if value.endswith('k'):
            multiplier = 1000
            value = value[0:len(value)-1] # strip multiplier character
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1] # strip multiplier character
        return int(float(value) * multiplier)


def get_r_values():
    MAX_PAGE = 11
    all_r = []
    for i in range(1,11):
        url =  "https://www.digikey.com/product-search/download.csv?FV=c0001%2Cc0163%2Cc0172%2Cc0179%2Cc017c%2C142c07b9%2Cmu10kOhms%7C2085%7C0%2Cmu200kOhms%7C2085%7C1%2Cffe00034&quantity=0&ColumnSort=0&page={}&stock=1&pageSize=500".format(i)
        data = urllib.request.urlopen(url).read()
        output = data.decode('utf-8')
        datas_file = open("hurr.csv",'w')
        datas_file.write(output)
        datas_file.close()
        
        f = StringIO(output)
        csv_data = csv.DictReader(f,delimiter=",")
        for row  in  csv_data:
            m = re.search('(.*)Ohms',row["Resistance"])
            striped = re.sub(r'\s+', '',m.group(1))
            all_r.append(convert(striped))
    print(len(all_r))
    
def convert(value):
    if value:
        # determine multiplier
        multiplier = 1
        if value.endswith('k'):
            multiplier = 1000
            value = value[0:len(value)-1] # strip multiplier character
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1] # strip multiplier character
        return int(float(value) * multiplier)


def get_r_values():
    MAX_PAGE = 11
    all_r = []
    for i in range(1,11):
        url =  "https://www.digikey.com/product-search/download.csv?FV=c0001%2Cc0163%2Cc0172%2Cc0179%2Cc017c%2C142c07b9%2Cmu10kOhms%7C2085%7C0%2Cmu200kOhms%7C2085%7C1%2Cffe00034&quantity=0&ColumnSort=0&page={}&stock=1&pageSize=500".format(i)
        data = urllib.request.urlopen(url).read()
        output = data.decode('utf-8')
        datas_file = open("hurr.csv",'w')
        datas_file.write(output)
        datas_file.close()
        
        f = StringIO(output)
        csv_data = csv.DictReader(f,delimiter=",")
        for row  in  csv_data:
            m = re.search('(.*)Ohms',row["Resistance"])
            striped = re.sub(r'\s+', '',m.group(1))
            all_r.append(convert(striped))
    print(len(list(sorted(set(all_r)))))
    return(list(sorted(set(all_r))))


def calc_values(values):
    for r1_val in values:
        for r2_val in values:
            for r3_val in values:
                val_high = REG_REF_VOLTAGE*(1 + (r1_val/r2_val)) + (REG_REF_VOLTAGE - DACV_LOW) * (r1_val/r3_val)
                if val_high < MAX_REG_VOLTAGE and val_high > MAX_REG_VOLTAGE - MAX_VOLT_DEV:
                    val_low = REG_REF_VOLTAGE*(1 + (r1_val/r2_val)) + (REG_REF_VOLTAGE - DACV_HIGH) * (r1_val/r3_val)
                    if val_low > MIN_REG_VOLTAGE and val_low < MIN_REG_VOLTAGE + MAX_VOLT_DEV:
                        print("Low: {} High: {} ".format(val_high,val_low))
                        print("R1 : {} R2 :{} R3:{}\n\r".format(r1_val,r2_val,r3_val))

#VOUT = VREF(1 + (R1/R2)) + (VREF - VDAC) (R1/R3)

if __name__ == "__main__":
    values = get_r_values()
    calc_values(values)
        
                
                
    
    
    
