#!/usr/bin/env bash

# Download campaign contribution data from the Federal Election Commission and unzip it
wget https://www.fec.gov/files/bulk-downloads/data_dictionaries/indiv_header_file.csv
wget https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip
unzip indiv20.zip

# Download and unzip the ZIP code data
wget https://simplemaps.com/static/data/us-zips/1.7/basic/simplemaps_uszips_basicv1.7.zip
unzip simplemaps_uszips_basicv1.7.zip

# Download 2018 population estimates for US counties
wget https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/asrh/cc-est2018-alldata.csv
