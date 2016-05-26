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

    try:
        with open(file) as csv_file:
            basedata = DictReader(csv_file)
            for row in basedata:
                all_rows.append(row)
                if count > 0 and int(row['ZTIME']) not in years:
                    break
                if int(row['ZTIME']) in years:
                    #print(row['ZTIME'])

                    count += 1
                    expected_prices(all_rows)



    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(e.errno)
    except:
        print("Error please check your conditional statements")

def expected_prices(rows):
    current_row = rows[-1]
    past_row = rows[-2]
    #print("current row: ", current_row)
    #return price

    price = ((.253 + .747 * float(past_row['CRSYLD1']))/ float(past_row['CREYLD1']))
    print(price)



#return price

main()