#!/usr/bin/env python2.7
import os
import csv
import time

with open('../resources/USDAPlantList.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    commons = []
    scientifics = []
    # read every line
    for row in reader:
        if line_count == 0:
            print("Column names are: %s" % (row))
            line_count = line_count + 1
        else:
            # take the necessary info out
            scientific = ' '.join(row[2].split()[0:2])
            common = row[3]
            if len(common) <= 1:
                common = scientific
            commons.append(common)
            scientifics.append(scientific)
            line_count = line_count + 1

    # write formatted data
    with open("USDA_plants.txt","w") as file:
        for common, scientific in zip(commons,scientifics):
            file.write("{\"name\": \"%s\",\n\"scientificName\": \"%s\",\n\"resolution\": \"%s\"},\n\n" % (common, scientific,"house"))

