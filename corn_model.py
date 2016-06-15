from csv import DictReader
import pandas as pd
import scipy as sy
import matplotlib.pyplot as plt
import numpy as np



# Years
starting_year = 2014
ending_year = 2023

years = range(starting_year, ending_year + 1)



def main():
    count = 0
    # name of the file
    file = "data.csv"
    all_rows = []

    try:
        with open(file) as csv_file:
            basedata = DictReader(csv_file)
            for row in basedata:
                all_rows.append(row)
                if(int(row['YEAR']) in years):

                    print("Corn expected market price: ", cemp(all_rows))
                    print("Corn expected yield: ", cey(all_rows))

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(e.errno)
    except ValueError:
        print("ValueError")

# Nominal reference price (Deflator)
def nfp(rows):
    print("hello")


# Corn expect market price
def cemp(rows):
    current_year = rows[-1]
    price = float(current_year['prPPCO']) - float(current_year['prEPCOmkt'])
    return price

# Corn expect yield
def cey(rows):
    current_year = rows[-1]

    cyield = -2.28290274642977 + 0.107815751601678 * (int(current_year['YEAR']) - 1900) - float(current_year['crYECOto'])
    return cyield

main()
