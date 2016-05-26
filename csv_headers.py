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
                    gross_return.append(expected_market_gross_return(all_rows))
                    rt_1, rt_2 = LDG_and_MLG_actual_expected (all_rows)
                    lda_mlg_rt1.append(rt_1)
                    lda_mlg_rt2.append(rt_2)
        print("Expected Prices: ", ex_prices)
        print("Gross return: ", gross_return)
        print(lda_mlg_rt1)
        print(lda_mlg_rt2)



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


def expected_market_gross_return(rows):
    current_year = rows[-1]
    gross = float(current_year['CREPFM1']) * float(current_year['CREYLD1'])
    return gross

def LDG_and_MLG_actual_expected (rows):
    current_year, previous_year = rows[-1], rows[-2]
    rate1 = 0.25 * max(0, float(previous_year['CRPLNR1']) + 0.40 - float(current_year['CRPFRM'])) + \
            0.5 * max(0, float(previous_year['CRPLNR1']) + 0.20 - float(previous_year['CRPFRM'])) + \
            0.25 * max(0, float(previous_year['CRPLNR1']) - float(current_year['CRPFRM']) + float(current_year['CRE4']))


    rate2 = 0.25 * max(0, float(current_year['CRPLNR1']) + 0.40 - float(previous_year['CREPFM1'])) + \
            0.5 * max(0, float(current_year['CRPLNR1']) + 0.20 - float(current_year['CREPFM1'])) + \
            0.25 * max(0, float(current_year['CRPLNR1']) - float(previous_year['CREPFM1']))

    return rate1, rate2

main()