#!/usr/bin/env python2.7
import os

commands = []
path ="../resources/Plant_images/.DS_Store"

if os.path.isfile(path):
    commands.append("rm " + path)
commands.append("gsutil -m cp -r /Users/felipearce/go/src/github.com/astherath/autoMLtest/model_training/resources/Plant_images gs://automl-test-251018-vcm/")
commands.append("./csv_writer.py")
commands.append("mv training_data.csv ..")
commands.append("gsutil cp /Users/felipearce/go/src/github.com/astherath/autoMLtest/model_training/training_data.csv gs://automl-test-251018-vcm/")

final_command = ""
for command in commands:
    final_command = final_command + command + " && "

os.system(final_command)
