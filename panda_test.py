import pandas as pd
from scipy import optimize
import numpy as np
# from pandas import Series, DataFrame

start_year = int(2014)
end_year = int(2023)
first_year = 1981
YEAR,prRPCO,prRPCOnom,\
prPPCO,prEPCOmkt,crYECOto,\
prVCCO,DOMDEF,e_prPPCO,\
Y262_EMktRct,prENCOmkt,\
prENSRmkt,prENWHmkt,prENCTmkt,\
prENSB,crAPCOpri,crAPCOto,\
e_crAPCOto,crAHCOto,e_crAHCOto,\
Fert_PPI,e_crYLCOto,crYLCOto,\
crPRCOto,crIMCOto,e_crIMCOto,\
crSYCOto,crESCOto,crEXCOto,\
lsPRHGjpn,Hog_PrdEU6,Hog_PrdUK,\
SDR_exch,e_crEXCOto,crDMCOOT,POP,\
prPPWH,All_CPI,RealDispInc,Crn_SeedRate,\
e_crDMCOFD,crDMCOFD,crDMCOFE,crDMCOto,\
GCAU,prCPSM,LivestockP,prPPSR,prPPBA,\
prPPOC,e_crDMCOFE,e_crESCOto = range(0,52)




t = np.array(range(start_year-first_year, end_year + 1 - first_year))
vals = (np.where(t > 2016, 1, 0))


def model(d2):

    # d2: data frame with all values
    # returns: data frame with values updated by equatiosn

    # Nominal reference price (Deflator)
    d2.ix[t, prRPCOnom] = d2.ix[t, prRPCO] * d2.ix[t, DOMDEF] / 100

    # Corn farm price
    d2.ix[t, prPPCO] = .816 * d2.ix[t, prRPCOnom] + d2.ix[t, e_prPPCO]

    # Corn expect market price
    d2.ix[t, prEPCOmkt] = d2.ix[t, prPPCO]

    # Corn expect yield
    d2.ix[t, crYECOto] = -2.28290274642977 + 0.107815751601678 * (t + 1981 - 1900)

    # Corn expected revenue
    d2.ix[t, Y262_EMktRct] = d2.ix[t, prEPCOmkt] * d2.ix[t, crYECOto]

    # Corn expect mkt net return
    d2.ix[t, prENCOmkt] = d2.ix[t, Y262_EMktRct] - d2.ix[t, prVCCO]

    # Corn planted area, price component
    d2.ix[t, crAPCOpri] = (10.611101118283 * d2.ix[t, prENCOmkt] - 0.902382503422328 * d2.ix[t, prENSRmkt] -
                             1.47558373064159 * d2.ix[t, prENWHmkt] - 0.245657668808256 * d2.ix[t, prENCTmkt] -
                             6.83910949962186 * d2.ix[t, prENSB])

    # # Behav. corn area planted
    equ = []
    for x in np.nditer(t-2014):
        equ.append(1.15**x)

    d2.ix[t, crAPCOto] = pd.Series(.5*d2.ix[t,crAPCOpri].values+ .3 * d2.ix[t - 1,crAPCOpri].values + .2 *
                            d2.ix[t - 2, crAPCOpri].values+np.where(t + 1981 > 2016, 1, 0) * 40*
                            np.array(equ) + d2.ix[t, e_crAPCOto].values, index=d2.ix[t,crAPCOpri].index)#(t-2014) +d2.ix[t, 'e_crAPCOto'].reset_index(drop=True))


    # # Corn area harvested
    # d2[t, crAHCOto] = pd.Series(0.758855 * d2.ix[t - 1, crAPCOto].values + 1.499 *
    #                         ((t - 1) - 1900)*d2.ix[t-1, crAPCOto].values / 1000
    #                         + d2.ix[t, e_crAHCOto].values, index=d2.ix[t, e_crAHCOto].index)

    # Corn yield
    d2.ix[t, crYLCOto] = pd.Series(0.108737105543302 * ((t + 1981- 1) - 1900) + 0.0913912636493641 *
                                     d2.ix[t - 1, prPPCO].values /
                                     d2.ix[t - 1, Fert_PPI].values + d2.ix[t, e_crYLCOto].values,
                                     index=d2.ix[t, e_crYLCOto].index)

    # Corn production
    d2.ix[t, crPRCOto] = d2.ix[t, crYLCOto] * d2.ix[t, crAHCOto]

    # Corn imports
    # d2.ix[t, crIMCOto] = (d2.ix[t - 1, crIMCOto].reset_index(drop=True) + 2
    #                         * d2.ix[t - 1, crIMCOto].reset_index(drop=True) *  (d2.ix[t, prPPCO]/
    #                                                                               d2.ix[t - 1, prPPCO].reset_index(drop=True) - 1) +
    #                         d2[t, e_crIMCOto].reset_index(drop=True))

    d2.ix[t, crIMCOto] = np.where(d2.ix[t, crIMCOto] < 0, 0, d2.ix[t, crIMCOto])  # don't let imports be negative

    # Corn supply
    d2.ix[t, crSYCOto] = d2.ix[t - 1, crESCOto].reset_index(drop=True)  + d2.ix[t, crPRCOto] + d2.ix[t, crIMCOto]

    # Behavioral corn exports
    d2.ix[t, crEXCOto] = (2.96502892559359 * d2.ix[t, lsPRHGjpn] + 2.96502892559359 * d2.ix[t, Hog_PrdEU6] +
                            2.96502892559359 * d2.ix[t, Hog_PrdUK] - 441.214299056417 * d2.ix[t, prPPCO] /
                            d2.ix[t, SDR_exch] + d2.ix[t, e_crEXCOto])

    # Corn for fuel, just hard coded in

    # Corn FSI (food, seed, indust incl alc)
    d2.ix[t, crDMCOFD] = (d2.ix[t, crDMCOOT] - 99.0995281730836 * d2.ix[t, POP] + 1.50026988753628 *
                            d2.ix[t, POP] * ((t - 1 + 1981) - 1900) + 6.15613730393188 * d2.ix[t, prPPWH] /
                            d2.ix[t, All_CPI] * d2.ix[t, POP] - 14.8824052828484 * d2.ix[t, prPPCO] /
                            d2.ix[t, All_CPI] * d2.ix[t, POP] + 1649.07060892978 * d2.ix[t, RealDispInc] +
                            1.13148382687209 * d2.ix[t, crAPCOto] * d2.ix[t+1, Crn_SeedRate] / 1000 +
                            d2.ix[t, e_crDMCOFD])

    # Corn feed & resid (not sure if this is the correct equation to use)
    d2.ix[t, crDMCOFE] = pd.Series(471.267379169762 * d2.ix[t, GCAU].values + 0.248861330680676 * d2.ix[t, prCPSM].values
                            / d2.ix[t, LivestockP].values * d2.ix[t, GCAU].values + 1.26455907960682 * d2.ix[t, prPPSR].values
                            / d2.ix[t, LivestockP].values * d2.ix[t, GCAU].values + 0.427654411065806 * d2.ix[t, prPPBA].values
                            / d2.ix[t, LivestockP].values * d2.ix[t, GCAU].values + 0.831092830565033 * d2.ix[t, prPPOC].values
                            / d2.ix[t, LivestockP].values * d2.ix[t, GCAU].values - 5.18301435157038 * d2.ix[t, prPPCO].values
                            / d2.ix[t, LivestockP].values * d2.ix[t, GCAU].values + 0.624418 * d2.ix[t - 1, crDMCOFE].values
                            * d2.ix[t, GCAU].values / d2.ix[t - 1, GCAU].values + d2.ix[t, e_crDMCOFE].values,
                                     index=d2.ix[t, LivestockP].index)

    # Corn dom disapp
    d2.ix[t, crDMCOto] = d2.ix[t, crDMCOFD] + d2.ix[t, crDMCOFE]

    # Corn stocks (also not sure if this is the correct one to use)
    d2.ix[t, crESCOto] = - 90 * d2.ix[t, prPPCO] + 0.4 * d2.ix[t, crPRCOto] + d2.ix[t, e_crESCOto]

    return d2


def closing_equation(d1):
    # x: array of values to try as solution
    # d1: data frame with all variables
    # returns: array of closing equation values
    #print(d1)
    d1.shape = (46,52)
    #print(d1)
    d1 = pd.DataFrame(d1)
    #print(d1)
    d1 = model(d1)
    eqs = d1.ix[t,crSYCOto] - d1.ix[t,crEXCOto] + d1.ix[t, crDMCOto] + d1.ix[t, crESCOto]
    d1 = d1.values
    d1 = np.reshape(d1, (2392))
    #print(d1)
    return d1

def main():
    file = "data.csv"

    basedata = pd.read_csv(file)
    s = basedata.copy()
    #print(s)


    model_data = model(s)

    #eqs = model_data.ix[t, crSYCOto] - model_data.ix[t, crEXCOto] + model_data.ix[t, crDMCOto] + model_data.ix[t, crESCOto]

    print(model_data - basedata)
    #print(model_data.ix[t, 'crAPCOto']-basedata.ix[t, 'crAPCOto'])

    sol = optimize.root(closing_equation, s.values, method='hybr')
    print(sol)

    #rint(s.ix[t-1,'crAPCOpri'].add(s.ix[t, 'crAPCOpri'], fill_value=s.ix[t-1,'crAPCOpri']))
    #print(s.ix[t, 'crAPCOpri'].swaplevel(-2,-1,True))
    #print(pd.Series(s.loc[t, 'crAPCOpri'].values + s.loc[t-1, 'crAPCOpri'].values, index=s.loc[t, 'crAPCOpri'].index))
    #print(val)
    #print(val1)

    #print(np.array(.5 * s.loc[t, 'crAPCOpri'] + .3 * s.loc[t - 1, 'crAPCOpri'] + .2 * s.loc[t-2, 'crAPCOpri']))
    # print(np.where(t > 2016, 1, 0) * 40)

main()
