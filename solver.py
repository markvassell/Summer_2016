from scipy import optimize
from csv import DictReader
import pandas as pd
import numpy as np
from decimal import *
import matplotlib.pyplot as plt







def equilibrium (rows):


     current_year = rows[-1]

     return [float(current_year['prRPCO'],(float(current_year['crSYCOto']) - float(current_year['crEXCOto']) + float(current_year['crDMCOto']) +
             float(current_year['crESCOto']]



def main():
    starting_year = 2014
    ending_year = 2024
    years = range(starting_year, ending_year+1)
    active_rows = list()
    file = "data.csv"

    #try:
    with open(file) as csv_file:
        basedata = DictReader(csv_file)
        for row in basedata:
            active_rows.append(row)
            if (int(row['YEAR']) in years):
                #print(equilibrium(active_rows).)

                sol = optimize.root(equilibrium, [0, 0], method='hybr')
                print(sol.x)
    #except:
        #print("error")





if __name__ == "__main__":
    main()