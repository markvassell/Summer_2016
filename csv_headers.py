from csv import DictReader
import matplotlib.pyplot as plt
from collections import defaultdict

starting_year = 2014
ending_year = 2024


years = range(starting_year, ending_year + 1)
def main():
    count = 0
    file = "crop_data.csv"
    all_rows = []

    gross_return, ex_prices, lda_mlg_rt1, lda_mlg_rt2, net_returns = list(),list(), list(), list(), list()
    harv_area, c_yield, production, feed, usage = list(), list(), list(), list(), list()

    try:
        with open(file) as csv_file:
            basedata = DictReader(csv_file)
            for row in basedata:
                all_rows.append(row)
                if count > 0 and int(row['ZTIME']) not in years:
                    break
                if int(row['ZTIME']) in years:
                    count += 1
                    ex_prices.append(expected_prices(all_rows))





    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(e.errno)
    except:
        print("Error please check your conditional statements")

def expected_prices(rows):
    current_year = rows[-1]
    previous_year = rows[-2]
    price = ((.253 + .747 * float(previous_year['CRSYLD1'])/ float(previous_year['CREYLD1']) + \
              float(current_year['CRE3'])) *float(current_year['CRPFRM']))
    return(price)


main()