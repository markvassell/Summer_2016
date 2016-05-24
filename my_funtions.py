from scipy.stats import logistic
from math import exp
def expected_prices(c_list, headers, row):


    price = ((.253 + .747 *
              float(c_list[row - 1][headers['CRSYLD1']]) /
              float(c_list[row - 1][headers['CREYLD1']]) +
              float(c_list[row][headers['CRE3']])) *
             float(c_list[row][headers['CRPFRM']]))
    return price
def expected_market_gross_return(c_list, headers, row):
    gross = (float(c_list[row][headers['CREPFM1']])) * (float(c_list[row][headers['CREYLD1']]))
    return gross
def LDG_and_MLG_actual_expected (csv_list, dictionary_of_headers, row):
    rate1 = 0.25 * max(0, float(csv_list[row - 1][dictionary_of_headers['CRPLNR1']]) +
                       0.40 - float(csv_list[row][dictionary_of_headers['CRPFRM']])) +\
            0.5*max(0, float(csv_list[row - 1][dictionary_of_headers['CRPLNR1']]) +
                    0.20 - float(csv_list[row - 1][dictionary_of_headers['CRPFRM']])) + \
            0.25*max(0, float(csv_list[row - 1][dictionary_of_headers['CRPLNR1']]) -
                     float(csv_list[row][dictionary_of_headers['CRPFRM']]) +
                     float(csv_list[row][dictionary_of_headers['CRE4']]))

    rate2 = 0.25 * max(0, float(csv_list[row][dictionary_of_headers['CRPLNR1']])
                       + 0.40 - float(csv_list[row][dictionary_of_headers['CREPFM1']])) +\
            0.5*max(0, float(csv_list[row][dictionary_of_headers['CRPLNR1']])
                    + 0.20 - float(csv_list[row][dictionary_of_headers['CREPFM1']])) + \
            0.25*max(0, float(csv_list[row][dictionary_of_headers['CRPLNR1']])
                     - float(csv_list[row][dictionary_of_headers['CREPFM1']]))

    return rate1, rate2

def get_corn_net_returns(c_list, headers, row):
    net = float(c_list[row][headers['CREMGR1']]) + \
          float(c_list[row][headers['CRELDPA1']]) * \
          float(c_list[row][headers['ATBL1']]) +\
          .25 * (1 - float(c_list[row][headers['CRACRPR1']])) * \
          float(c_list[row][headers['CRECCPA1']]) +\
          0.75 *float(c_list[row][headers['CICRPRS1']]) / \
          float(c_list[row][headers['CRSPLT1']]) +\
          (1 * (1 - float(c_list[row][headers['COARCPT1']]))
           + .25 * float(c_list[row][headers['COARCPT1']]))\
            * float(c_list[row][headers['CRACRPR1']]) \
          * float(c_list[row][headers['CREACAC1']]) - \
          float(c_list[row][headers['CRVARC1']])


    return net

def get_corn_area(c_list, headers, row):
    area = (float(c_list[row][headers['CRSPLT1']])) * (float(c_list[row][headers['CRHPRAT1']]))
    return area

def cal_corn_yield(c_list, headers, row):
    #the year for the current row is stored in the first index of c_list. Example float(c_list[row][0]) = 2014
    c_yield = 94.1206 + 0.6488 * ((float(c_list[row][headers['CRENRS1']])) + (float(c_list[row][headers['CRVARC1']])))\
                 / (float(c_list[row][headers['CRVARC1']])) + 4.6159 / 10 \
                                                              * ((float(c_list[row][headers['CRENRS1']]) + float(c_list[row][headers['CRVARC1']]))
                                                                 / float(c_list[row][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 1][headers['CRENRS1']]) + float(c_list[row - 1][headers['CRVARC1']]))
                                                                 / float(c_list[row - 1][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 2][headers['CRENRS1']]) + float(c_list[row - 2][headers['CRVARC1']]))
                                                                 / float(c_list[row - 2][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 3][headers['CRENRS1']]) + float(c_list[row - 3][headers['CRVARC1']]))
                                                                 / float(c_list[row - 3][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 4][headers['CRENRS1']]) + float(c_list[row - 4][headers['CRVARC1']]))
                                                                 / float(c_list[row - 4][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 5][headers['CRENRS1']]) + float(c_list[row - 5][headers['CRVARC1']]))
                                                                 / float(c_list[row - 5][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 6][headers['CRENRS1']]) + float(c_list[row - 6][headers['CRVARC1']]))
                                                                 / float(c_list[row - 6][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 7][headers['CRENRS1']]) + float(c_list[row - 7][headers['CRVARC1']]))
                                                                 / float(c_list[row - 7][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 8][headers['CRENRS1']]) + float(c_list[row - 8][headers['CRVARC1']]))
                                                                 / float(c_list[row - 8][headers['CRVARC1']]) +
                                                                 (float(c_list[row - 9][headers['CRENRS1']]) + float(c_list[row - 9][headers['CRVARC1']]))
                                                                 / float(c_list[row - 9][headers['CRVARC1']])) - \
                0.0146 * (float(c_list[row][headers['USPLT1']])) - 0.0406 * (float(c_list[row][headers['CRSPLT1']])) \
                + 1.8950 * ((float(c_list[row][0])) - 1979) + float(c_list[row][headers['CRE2']])

    return c_yield

def cal_production(c_list, headers, row):

    value = float(c_list[row][headers['CRSHAR1']]) * float(c_list[row][headers['CRSYLD1']])
    return value

def cal_corn_feed(c_list, headers, row):

    total = (0.68 - 0.0641475 * float(c_list[row][headers['CRPFRM']]) / float(c_list[row][headers['LPIGCAU']]) -
             0.65858 * (1.13 * float(c_list[row][headers['WHDFED']]) + 0.95 * float(c_list[row][headers['SGDFED']])
                        + 0.77 * float(c_list[row][headers['BRDFED']]) + 0.51 * float(c_list[row][headers['OTDFED']]))
             / float(c_list[row][headers['GCAU']]) - 0.55 * float(c_list[row][headers['GFDDOM']]) * 2 / 56 /
             float(c_list[row][headers['GCAU']]) + 0.0004275 * float(c_list[row][headers['SMP48D']]) /
             float(c_list[row][headers['LPIGCAU']]) - 0.0100 * max(0, float(c_list[row][headers['CRPFRM']])
                                                                   * 2000 / 56 * 1.1 -
                                                                   float(c_list[row][headers['SMP48D']]))
             * 2 / 56 * float(c_list[row][headers['HPAU']]) / float(c_list[row][headers['GCAU']]) + 0.16689 *
             float(c_list[row - 1][headers['CRSPRD1']]) / float(c_list[row][headers['GCAU']]) - 1.1 *
             (float(c_list[row][headers['DGCONBE']]) * float(c_list[row][headers['DGDCOBE']]) +
              float(c_list[row][headers['DGCONPK']]) * float(c_list[row][headers['DGDCOPK']]) +
              float(c_list[row][headers['DGCONBR']]) * float(c_list[row][headers['DGDCOBR']]) +
              float(c_list[row][headers['DGCONDY']]) * float(c_list[row][headers['DGDCODY']]))
             * 2 / 56 / float(c_list[row][headers['GCAU']]) + float(c_list[row][headers['CRE22']])) * \
            float(c_list[row][headers['GCAU']])

    return total

def cal_seeds_used(c_list, headers, row):
    usage = (0.2400 + 0.0153 * float(c_list[row][headers['SHIFT84']]) + float(c_list[row][headers['CRE23']])) * \
            float(c_list[row][headers['CRSPLT1']])
    return usage
# plogis funtion from R. Distribution function. CDF
def distribution_function(val, m, s):
    return (1 / (1 + exp(-(val - m) / s)))

def cal_loan_stocks(c_list, headers, row):
    # loan = distribution_function(-.698 - 1.5955 * (float(c_list[count][headers['CRPFRM']]) +
    #                                                float(c_list[count][headers['CRLDPRT']]))/
    #                              float(c_list[count - 1][headers['CRPLNR1']]) - 0.694 *
    #                              float(c_list[count][headers['SHIFT93']]) + float(c_list[count][headers['CRE27']]),0,1)\
    #         * float(c_list[count - 1][headers['CRSPRD1']])
    loan = logistic.cdf(-.698 - 1.5955 * (float(c_list[row][headers['CRPFRM']]) +
                                          float(c_list[row][headers['CRLDPRT']])) /
                        float(c_list[row - 1][headers['CRPLNR1']]) - 0.694 *
                        float(c_list[row][headers['SHIFT93']]) + float(c_list[row][headers['CRE27']])) \
            * float(c_list[row - 1][headers['CRSPRD1']])
    return loan


def solve_comm1(c_list, headers, row):
    value = float(c_list[row - 1][headers['CRSPRD1']]) + float(c_list[row - 1][headers['CRSIMP1']]) + \
            float(c_list[row - 1][headers['CRDFOR']]) + float(c_list[row - 1][headers['CRDCCC']]) + \
            float(c_list[row - 1][headers['CRD9MO']]) + float(c_list[row - 1][headers['CRDFRE']]) - \
            float(c_list[row][headers['CRDFED']]) - float(c_list[row][headers['CRDSED']]) - \
            float(c_list[row][headers['CRDFOD']]) - float(c_list[row][headers['CRDHFC']]) - \
            float(c_list[row][headers['CRDGAS']]) - float(c_list[row][headers['CRDEXP']]) - \
            float(c_list[row][headers['CRDFRE']]) - float(c_list[row][headers['CRD9MO']]) - \
            float(c_list[row][headers['CRDCCC']]) - float(c_list[row][headers['CRDFOR']])
    return value

def append_to_array(array, headers, the_list, name, row):
    array.append()