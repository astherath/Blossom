#!/usr/bin/env python2.7
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from timeout import timeout
import time
import json
import os
import urllib2
import argparse

plantindex = 0
imgs_requested = 1000
base_dir = "resources/Plant_images/"

# defines a plant object
class Plant:
    def __init__(self,scientific,common):
        self.scientific = scientific
        self.common = common

def save(plant, complete, index, plant_index):
    with open("downloaded.json","w") as File:
        # break down the plant object
        common = plant.common
        scientific = plant.scientific
        # change bool to string to fit json format
        if complete:
            complete_str = "true"
        else:
            complete_str = "false"

        File.write("""{\n\"lastDownload\":\n{\"complete\": %s,
                \n\"name\": \"%s\",\n\"scientificName\": \"%s\",
                \n\"lastDownloadedIndex\": %d,\n\"plantIndex\": %d\n}}""" % (complete_str, common, scientific, index, plant_index))

def check():
    if os.path.isfile('downloaded.json'):
        with open('downloaded.json','r') as File:
            downloaded = json.load(File)["lastDownload"]
            completed = downloaded["complete"]
            if not completed:
                current_index = downloaded["lastDownloadedIndex"]
                current_plant = downloaded["plantIndex"]
                return (current_index, current_plant)
            else:
                return (-1, -1)
    else:
        return (-1,-1)

def scrape(plant):
    # break down the plant object
    common = plant.common
    scientific = plant.scientific
    start_time = time.time()
    # opening client
    url = "https://www.google.co.in/search?q="+scientific+"&source=lnms&tbm=isch"
    browser = webdriver.Chrome()
    browser.get(url)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    counter = 0
    succounter = 0

    if not os.path.exists(base_dir + common):
        os.mkdir(base_dir + common)

    for i in range(80):
        browser.execute_script("window.scrollBy(0,10000)")
        time.sleep(0.1)
        try:
            show_more_button = browser.find_element_by_id("smb")
            show_more_button.click()
        except:
            continue

    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter = counter + 1
        print "Total Count:", counter
        print "Succsessful Count:", succounter
        print "URL:",json.loads(x.get_attribute('innerHTML'))["ou"]

        img = json.loads(x.get_attribute('innerHTML'))["ou"]
        imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
        try:
            @timeout(20)
            def try_download():
                req = urllib2.Request(img, headers={'User-Agent': header})
                raw_img = urllib2.urlopen(req).read()
                File = open(os.path.join(base_dir, common , common + "_" + str(counter) + "." + imgtype), "wb")
                File.write(raw_img)
                File.close()
            try_download()
            succounter = succounter + 1
            if succounter >= imgs_requested:
                break
            # deciding when to save download progress
            elif (succounter % 10 == 0) or (succounter == 1):
                complete = plantindex == len(plants) - 1
                save(plant, complete, succounter, plantindex)

        except Exception as e:
            print(e)

    browser.close()
    elapsed_time = time.time() - start_time
    print succounter, "pictures succesfully downloaded in", elapsed_time, "seconds"

def pickup_scrape(plant, pickup_index):
    # break down the plant object
    common = plant.common
    scientific = plant.scientific
    start_time = time.time()
    succounter = pickup_index
    # opening client
    url = "https://www.google.co.in/search?q="+scientific+"&source=lnms&tbm=isch"
    browser = webdriver.Chrome()
    browser.get(url)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    counter = 0
    succounter = 0

    if not os.path.exists(base_dir + common):
        os.mkdir(base_dir + common)

    for i in range(80):
        browser.execute_script("window.scrollBy(0,10000)")
        time.sleep(0.1)
        try:
            show_more_button = browser.find_element_by_id("smb")
            show_more_button.click()
        except:
            continue

    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        pickup = pickup_index > counter
        if not pickup:
            print "Total Count:", counter
            print "Succsessful Count:", succounter
            print "URL:",json.loads(x.get_attribute('innerHTML'))["ou"]
        else:
            print ("Catching up to last download... \n%d out of %d" % (counter,pickup_index))
        counter = counter + 1

        img = json.loads(x.get_attribute('innerHTML'))["ou"]
        imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
        try:
            req = urllib2.Request(img, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()
            if not pickup:
                @timeout(20)
                def try_download():
                    File = open(os.path.join(base_dir, common , common + "_" + str(counter) + "." + imgtype), "wb")
                    File.write(raw_img)
                    File.close()
                try_download()
                succounter = succounter + 1
            if succounter >= imgs_requested:
                break
            # deciding when to save download progress
            elif (succounter % 10 == 0) or (succounter == 1):
                complete = plantindex == len(plants) - 1
                save(plant, complete, succounter, plantindex)
        except Exception as e:
            print(e)

    browser.close()
    elapsed_time = time.time() - start_time
    print succounter, "pictures succesfully downloaded in", elapsed_time, "seconds"

# to store the querries
common_names = []
scientific_names = []
resolutions = []
# array of plant objects
plants = []


# read data from json file
with open('resources/plants.json') as json_file:
    _,pickup_index = check()
    data = json.load(json_file)
    for plant in data["plants"]["house-plants"]:
        scientific = plant["scientificName"]
        common = plant["name"]
        plants.append(Plant(scientific, common))

    if pickup_index < 0:
        for plant in plants:
            scrape(plant)
            plantindex = plantindex + 1
    else:
        pickup_scrape(plants[pickup_index],pickup_index)
        plantindex = plantindex + 1
        pickup_index  = pickup_index  + 1
        while pickup_index < len(plants):
            scrape(plants[pickup_index])
            plantindex = plantindex + 1
            pickup_index = pickup_index + 1

