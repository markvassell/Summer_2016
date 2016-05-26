import matplotlib.pyplot as plt
from collections import defaultdict
import my_funtions
from csv import reader
from numpy import genfromtxt

# The csv file is broken into two sections. The headers and the values.
# The headers are stored in a dictionary (dictionay_of_headers) and
# the values are stored in an 2d array. This makes indexing / finding
# specific rows and columns in the file easy.


def main():
    file_name = 'crop_data.csv'

    # Setting the range of years of years
    starting_year = 2014
    ending_year = 2024
    years = range(starting_year, ending_year + 1)

    #this dictionary holds all the headers of the csv file.
    # It is used to find the values in the array created from the csv.
    dictionary_of_headers = {}


    #opening the file, and adding the headers to a dictionary.
    try:
        file = open(file_name, 'r')
        converted_file = reader(file)
        index = 0
        s = csv_list = list(converted_file)
        for header in csv_list:
            for info in header:
                dictionary_of_headers.update({info: index})
                index+=1
            break
        file.close()

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(e.errno)

    # Places all the information from the csv (except headers) into a list / array.
    my_data = genfromtxt(file_name, delimiter=',')

    row = 0

    eqs = defaultdict(list)
    gross_return, ex_prices, lda_mlg_rt1, lda_mlg_rt2, net_returns = list(),list(), list(), list(), list()
    harv_area, c_yield, production, feed, usage = list(), list(), list(), list(), list()

    CRPFRM, CREMGR1, CRLDPRT, CRELDPR1, CRENRS1, CRSHAR1 = list(), list(), list(),list(), list(), list()
    CRSYLD1, CRSPRD1, CRDFED, CRDSED = [], [], [], []

    # Runtime O(n). loops through the list with all the data and run calculations for the specified years.
    for line in my_data:
        if line[0] in years:
            #print("year = %d" % int(line[0]))

            # Storing original values

            CRPFRM.append(csv_list[row][dictionary_of_headers["CRPFRM"]])
            CREMGR1.append(csv_list[row][dictionary_of_headers["CREMGR1"]])
            CRLDPRT.append(csv_list[row][dictionary_of_headers["CRLDPRT"]])
            CRELDPR1.append(csv_list[row][dictionary_of_headers["CRELDPR1"]])
            CRENRS1.append(csv_list[row][dictionary_of_headers["CRENRS1"]])
            CRSHAR1.append(csv_list[row][dictionary_of_headers["CRSHAR1"]])
            CRSYLD1.append(csv_list[row][dictionary_of_headers["CRSYLD1"]])
            CRSPRD1.append(csv_list[row][dictionary_of_headers["CRSPRD1"]])
            CRDFED.append(csv_list[row][dictionary_of_headers["CRDFED"]])
            CRDSED.append(csv_list[row][dictionary_of_headers["CRDSED"]])
            # **********************************************************************************************************

            # expected prices
            exp_prices = my_funtions.expected_prices(s, dictionary_of_headers, row)
            ex_prices.append(exp_prices)
            #s[row][dictionary_of_headers['CREPFM1']] = exp_prices

            # **********************************************************************************************************

            # expected market gross returns

            exp_market_gross_return = my_funtions.expected_market_gross_return(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CREMGR1']] = exp_market_gross_return
            gross_return.append(exp_market_gross_return)
            # **********************************************************************************************************

            # Average LDP and MLG rates, actual and expected

            LDP_and_MLG_rates1, LDP_and_MLG_rates2 = \
                my_funtions.LDG_and_MLG_actual_expected(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRLDPRT']] = LDP_and_MLG_rates1
            #s[row][dictionary_of_headers['CRELDPR1']] = LDP_and_MLG_rates2
            lda_mlg_rt1.append(LDP_and_MLG_rates1)
            lda_mlg_rt2.append(LDP_and_MLG_rates2)
            # **********************************************************************************************************

            # corn expected net returns

            corn_exp_net_returns = my_funtions.get_corn_net_returns(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRENRS1']] = corn_exp_net_returns
            net_returns.append(corn_exp_net_returns)
            # **********************************************************************************************************

            # corn harvested area

            corn_harvested_area = my_funtions.get_corn_area(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRSHAR1']] = corn_harvested_area
            harv_area.append(corn_harvested_area)
            # **********************************************************************************************************

            # corn yield

            corn_yield = my_funtions.cal_corn_yield(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRSYLD1']] = corn_yield
            c_yield.append(corn_yield)
            # **********************************************************************************************************

            # corn production

            corn_production = my_funtions.cal_production(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRSPRD1']] = corn_production
            production.append(corn_production)
            # **********************************************************************************************************

            # corn feed

            corn_feed = my_funtions.cal_corn_feed(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRDFED']] = corn_feed
            feed.append(corn_feed)
            # **********************************************************************************************************

            # corn seeds used

            seeds_used = my_funtions.cal_seeds_used(s, dictionary_of_headers, row)
            #s[row][dictionary_of_headers['CRDSED']] = seeds_used
            usage.append(seeds_used)
            # **********************************************************************************************************

            # corn 9-month loan stocks
            #
            # loan_stocks = my_funtions.cal_loan_stocks(s, dictionary_of_headers, row)
            # s[row][dictionary_of_headers['CRD9MO']] = loan_stocks

            # **********************************************************************************************************

            #comm1

            # value = my_funtions.solve_comm1(s, dictionary_of_headers, row)

            # s[count][dictionary_of_headers['comm1']]
            #
            # print("Expected prices: $%f" % exp_prices)
            # print("Expected gross return: $%f" % exp_market_gross_return)
            # print("Average LDP and MLG rates1: $%f" % LDP_and_MLG_rates1)
            # print("Average LDP and MLG rates2: $%f" % LDP_and_MLG_rates2)
            # print("Corn expected net returns: $%f" % corn_exp_net_returns)
            # print("Corn harvested area: %f" % corn_harvested_area)
            print("Corn yield: $%f" % corn_yield)
            # print("Corn production: %f" % corn_production)
            # print("Corn feed: %f" % corn_feed)
            # print("Corn seeds used: %f " % seeds_used)
            #  #print("corn 9-month loan stocks: ", loan_stocks)
            # print("Comm1: %f", value)

            #print()
            #exp_prices_list.append(exp_prices)
        row += 1
    eqs['CREPFM1'].append(ex_prices)
    eqs['CREMGR1'].append(gross_return)
    eqs['CRLDPRT'].append(lda_mlg_rt1)
    eqs['CRELDPR1'].append(lda_mlg_rt2)
    eqs['CRENRS1'].append(net_returns)
    eqs['CRSHAR1'].append(harv_area)
    eqs['CRSYLD1'].append(c_yield)
    eqs['CRSPRD1'].append(production)
    eqs['CRDFED'].append(feed)
    eqs['CRDSED'].append(usage)

    for i in eqs:
        print(i,eqs[i][0])

    plt.plot(years, CRPFRM,'bo',years, CRPFRM, 'k')
    plt.ylabel('basedata')
    plt.xlabel('Years')
    plt.show()



main()
