from csv import DictReader
import matplotlib.pyplot as plt


starting_year = 2014
ending_year = 2024


years = range(starting_year, ending_year + 1)


def main():
    count = 0
    #name of the file
    file = "crop_data.csv"
    all_rows = []
    # arrays to store all the values
    gross_return, ex_prices, lda_mlg_rt1, lda_mlg_rt2, net_returns = list(), list(), list(), list(), list()
    harv_area, c_yield, production, feed, usage = list(), list(), list(), list(), list()
    CRPFRM, CREMGR1, CRLDPRT, CRELDPR1, CRENRS1, CRSHAR1 = list(), list(), list(),list(), list(), list()
    CRSYLD1, CRSPRD1, CRDFED, CRDSED = [], [], [], []

    try:
        with open(file) as csv_file:
            basedata = DictReader(csv_file)
            for row in basedata:
                all_rows.append(row)
                # if all the years needed are found break the loop. Just make it small bit faster
                if count > 0 and int(row['ZTIME']) not in years:
                    break
                if int(row['ZTIME']) in years:
                    count += 1
                    # Storing original values
                    CRPFRM.append(row["CRPFRM"])
                    CREMGR1.append(row["CREMGR1"])
                    CRLDPRT.append(row["CRLDPRT"])
                    CRELDPR1.append(row["CRELDPR1"])
                    CRENRS1.append(row["CRENRS1"])
                    CRSHAR1.append(row["CRSHAR1"])
                    CRSYLD1.append(row["CRSYLD1"])
                    CRSPRD1.append(row["CRSPRD1"])
                    CRDFED.append(row["CRDFED"])
                    CRDSED.append(row["CRDSED"])

                    ex_prices.append(expected_prices(all_rows))
                    gross_return.append(expected_market_gross_return(all_rows))
                    rt_1, rt_2 = ldg_and_mlg_actual_expected(all_rows)
                    lda_mlg_rt1.append(rt_1)
                    lda_mlg_rt2.append(rt_2)
                    net_returns.append(get_corn_net_returns(all_rows))
                    harv_area.append(get_corn_area(all_rows))
                    c_yield.append(cal_corn_yield(all_rows))
                    production.append(cal_production(all_rows))
                    feed.append(cal_corn_feed(all_rows))
                    usage.append(cal_seeds_used(all_rows))

        print("Expected Prices: ", ex_prices)
        print("Gross return: ", gross_return)
        print(lda_mlg_rt1)
        print(lda_mlg_rt2)
        print("Net Returns: ", net_returns)
        print("Area: ", harv_area)
        print("Corn yield: ", c_yield)
        print("Corn production ", production)
        print("Corn feed: ", feed)
        print("Corn seed usage: ", usage)

        plt.plot(years, CRPFRM, 'bo', years, CRPFRM, 'k')
        plt.ylabel('basedata')
        plt.xlabel('Years')
        plt.show()

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(e.errno)
    except ValueError:
        print("ValueError")


def expected_prices(rows):
    current_year = rows[-1]
    previous_year = rows[-2]
    price = ((.253 + .747 * float(previous_year['CRSYLD1']) / float(previous_year['CREYLD1']) +
              float(current_year['CRE3'])) * float(current_year['CRPFRM']))
    return price


def expected_market_gross_return(rows):
    current_year = rows[-1]
    gross = float(current_year['CREPFM1']) * float(current_year['CREYLD1'])
    return gross


def ldg_and_mlg_actual_expected(rows):
    current_year, previous_year = rows[-1], rows[-2]
    rate1 = 0.25 * max(0, float(previous_year['CRPLNR1']) + 0.40 - float(current_year['CRPFRM'])) + \
        0.5 * max(0, float(previous_year['CRPLNR1']) + 0.20 - float(previous_year['CRPFRM'])) + \
        0.25 * max(0, float(previous_year['CRPLNR1']) - float(current_year['CRPFRM']) + float(current_year['CRE4']))

    rate2 = 0.25 * max(0, float(current_year['CRPLNR1']) + 0.40 - float(previous_year['CREPFM1'])) + \
        0.5 * max(0, float(current_year['CRPLNR1']) + 0.20 - float(current_year['CREPFM1'])) + \
        0.25 * max(0, float(current_year['CRPLNR1']) - float(previous_year['CREPFM1']))

    return rate1, rate2


def get_corn_net_returns(rows):
    current_year = rows[-1]
    net = float(current_year['CREMGR1']) + float(current_year['CRELDPA1']) * float(current_year['ATBL1']) + \
        .25 * (1 - float(current_year['CRACRPR1'])) * float(current_year['CRECCPA1']) + \
        0.75 * float(current_year['CICRPRS1']) / float(current_year['CRSPLT1']) +\
        (1 * (1 - float(current_year['COARCPT1'])) + .25 * float(current_year['COARCPT1'])) * \
        float(current_year['CRACRPR1']) * float(current_year['CREACAC1']) - float(current_year['CRVARC1'])

    return net


def get_corn_area(rows):
    current_year = rows[-1]
    area = (float(current_year['CRSPLT1'])) * (float(current_year['CRHPRAT1']))
    return area


def cal_corn_yield(rows):
    year_0 = rows[-1]
    year_1 = rows[-2]
    year_2 = rows[-3]
    year_3 = rows[-4]
    year_4 = rows[-5]
    year_5 = rows[-6]
    year_6 = rows[-7]
    year_7 = rows[-8]
    year_8 = rows[-9]
    year_9 = rows[-10]

    c_yield = 94.1206 + 0.6488 * ((float(year_0['CRENRS1'])) + (float(year_0['CRVARC1']))) \
                        / (float(year_0['CRVARC1'])) + 4.6159 / 10 * \
                                                       ((float(year_0['CRENRS1']) + float(year_0['CRVARC1'])) /
                                                        float(year_0['CRVARC1']) +
                                                       (float(year_1['CRENRS1']) + float(year_1['CRVARC1']))/
                                                        float(year_1['CRVARC1']) +
                                                        (float(year_2['CRENRS1']) + float(year_2['CRVARC1']))
                                                        / float(year_2['CRVARC1']) +
                                                        (float(year_3['CRENRS1']) + float(year_3['CRVARC1']))
                                                        / float(year_3['CRVARC1']) +
                                                        (float(year_4['CRENRS1']) + float(year_4['CRVARC1']))
                                                        / float(year_4['CRVARC1']) +
                                                        (float(year_5['CRENRS1']) + float(year_5['CRVARC1']))
                                                        / float(year_5['CRVARC1']) +
                                                        (float(year_6['CRENRS1']) + float(year_6['CRVARC1']))
                                                        / float(year_6['CRVARC1']) +
                                                        (float(year_7['CRENRS1']) + float(year_7['CRVARC1']))
                                                        / float(year_7['CRVARC1']) +
                                                        (float(year_8['CRENRS1']) + float(year_8['CRVARC1']))
                                                        / float(year_8['CRVARC1']) +
                                                        (float(year_9['CRENRS1']) + float(year_9['CRVARC1']))
                                                        / float(year_9['CRVARC1'])) - \
              0.0146 * (float(year_0['USPLT1'])) - 0.0406 * (float(year_0['CRSPLT1'])) \
              + 1.8950 * ((float(year_0['ZTIME'])) - 1979) + float(year_0['CRE2'])


    return c_yield

def cal_production(rows):
    current_year = rows[-1]

    value = float(current_year['CRSHAR1']) * float(current_year['CRSYLD1'])
    return value

def cal_corn_feed(rows):
    current_year = rows[-1]
    previous_year = rows[-2]

    total = (0.68 - 0.0641475 * float(current_year['CRPFRM']) / float(current_year['LPIGCAU']) -
             0.65858 * (1.13 * float(current_year['WHDFED']) + 0.95 * float(current_year['SGDFED'])
                        + 0.77 * float(current_year['BRDFED']) + 0.51 * float(current_year['OTDFED']))
             / float(current_year['GCAU']) - 0.55 * float(current_year['GFDDOM']) * 2 / 56 /
             float(current_year['GCAU']) + 0.0004275 * float(current_year['SMP48D']) /
             float(current_year['LPIGCAU']) - 0.0100 * max(0, float(current_year['CRPFRM'])
                                                                   * 2000 / 56 * 1.1 -
                                                                   float(current_year['SMP48D']))
             * 2 / 56 * float(current_year['HPAU']) / float(current_year['GCAU']) + 0.16689 *
             float(previous_year['CRSPRD1']) / float(current_year['GCAU']) - 1.1 *
             (float(current_year['DGCONBE']) * float(current_year['DGDCOBE']) +
              float(current_year['DGCONPK']) * float(current_year['DGDCOPK']) +
              float(current_year['DGCONBR']) * float(current_year['DGDCOBR']) +
              float(current_year['DGCONDY']) * float(current_year['DGDCODY']))
             * 2 / 56 / float(current_year['GCAU']) + float(current_year['CRE22'])) * \
            float(current_year['GCAU'])

    return total

def cal_seeds_used(rows):
    current_year = rows[-1]
    usage = (0.2400 + 0.0153 * float(current_year['SHIFT84']) + float(current_year['CRE23'])) * \
            float(current_year['CRSPLT1'])
    return usage
main()