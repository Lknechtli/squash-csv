#!/usr/bin/env python
"""
Dedupe a CSV using the first column as a primary key

Specify inputfile, outputfile, and optionally the csv delimiter
and separating symbol you want to use to separate the data from
rows which are combined
"""

import csv
import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    delimiter = ','
    symbol = ' | '
    try:
        opts, args = getopt.getopt(argv, "hi:o:d:s:", ["ifile=", "ofile=", "delimiter=", "symbol="])
    except getopt.GetoptError:
        print 'dedupe.py -i <inputfile> -o <outputfile>'
    for opt, arg in opts:
        if opt == '-h':
            print ('dedupe.py -i <inputfile> -o <outputfile>' +
                   '[-d <csv delimiter>] [-s <separating symbol>]')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--delimiter"):
            delimiter = arg
        elif opt in ("-s", "--symbol"):
            symbol = arg

    if not (inputfile and outputfile):
        print ('dedupe.py -i <inputfile> -o <outputfile>' +
               '[-d <csv delimiter>] [-s <separating symbol>]')
        sys.exit()

    print 'Deduping csv: ', inputfile
    print 'Into: ', outputfile
    data = {}
    header = []
    with open(inputfile, 'rb') as csvfile:
        hunchreader = csv.reader(csvfile, delimiter=delimiter)
        header = next(hunchreader, None)
        for row in hunchreader:
            if row[0] in data:
                for col in range(1, len(row)):
                    values = data[row[0]][col-1].split(symbol)
                    if row[col] != data[row[0]][col-1] and row[col] not in values:
                        data[row[0]][col-1] += symbol + row[col]
            else:
                data[row[0]] = row[1:]

    with open(outputfile, 'wb') as csvfile:
        hunchwriter = csv.writer(csvfile, delimiter=delimiter)
        hunchwriter.writerow(header)
        for key, value in data.items():
            hunchwriter.writerow([key]+value)
    print "\nDone."

if __name__ == "__main__":
    main(sys.argv[1:])
