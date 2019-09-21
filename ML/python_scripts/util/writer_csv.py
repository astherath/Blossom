#!/usr/bin/env python2.7
import os
import csv
import json


bucket_path = "gs://automl-test-251018-vcm/Plant_images/"
img_dirs = []
label_dirs = []
path = "/Users/felipearce/go/src/github.com/astherath/autoMLtest/model_training/resources/Plant_images"

label_dirs = os.listdir(path)

def write_imgs(label):
    label_dir = path + "/" + label
    img_dirs = os.listdir(label_dir)
    lines = []
    for img in img_dirs:
        current = bucket_path + label + "/" + img + "," + label
        lines.append(current)
    return lines

lines = []
for label in label_dirs:
    ls = write_imgs(label)
    for l in ls:
        lines.append(l)

with open('training_data.csv','w') as file:
    for line in lines:
        file.write(line + "\n")
