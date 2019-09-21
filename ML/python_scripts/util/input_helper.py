#!/usr/bin/env python2.7
import os

lines = []
#  with open("plants.txt","r") as file:
    #  lines = list(file)
def take_input():
    with open("plants.txt","w") as file:
        stop = False

        while not stop:
            common = raw_input("common name: ")
            scientific = raw_input("scientific name: ")

            if common == "stop" or scientific == "stop":
                stop = True
            else:
                file.write( "{\"name\": \"%s\",\n\"scientificName\": \"%s\",\n\"resolution\": \"photograph\"},\n\n" % (common, scientific))
def fix():
    odd = 1
    even = 0
    commons = []
    scientifics = []
    while even < len(lines) - 1:
        commons.append(lines[even].replace("\n",""))
        scientifics.append(lines[odd].replace("\n",""))
        odd = odd + 2
        even = even + 2

    with open("fixed_plants.txt","w") as file:
        for common, scientific in zip(commons,scientifics):
            file.write( "{\"name\": \"%s\",\n\"scientificName\": \"%s\",\n\"resolution\": \"%s\"},\n\n" % (common, scientific,"house"))

take_input()
