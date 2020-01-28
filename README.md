# CSE442 Assignment A2

Visualize individual campaign contribution data for the US from 2019 to 2020.

*This code is for assignment 2 for CSE 442, Data Visualization, at the University of Washington.*

## Installation

Install Python 3.6 and `pip` and install the following package

```
pip3 install pandas>=0.25.3
```


## Setup

Download campaign contribution data from the Federal Election Commission and unzip it,

```
wget https://www.fec.gov/files/bulk-downloads/data_dictionaries/indiv_header_file.csv
wget https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip
unzip indiv20.zip
```

Now download and unzip our ZIP code data,

```
wget https://simplemaps.com/static/data/us-zips/1.7/basic/simplemaps_uszips_basicv1.7.zip
unzip simplemaps_uszips_basicv1.7.zip
```

The files `indiv_header_file.csv`, `itcont.txt`, `zip_code_database.csv` should be in the working directory for this project.


## Data Preparation

To prepare our data for visualization, run

```
./prepare.py
```

This code may take some time to run. The code for extrapolating zip codes for incomplete rows is the current bottleneck.