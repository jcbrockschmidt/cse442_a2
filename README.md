# CSE442 Assignment A2

Visualize individual campaign contribution data for the US from 2019 to 2020.

*This code is for assignment 2 for CSE 442, Data Visualization, at the University of Washington.*

## Installation

Install Python 3.6 with `pip` and install the following packages,

```
pip3 install "pandas>=0.25.3" "altair>=4.0.1" "selenium>=3.141.0"
```

Download ChromeDriver for your version of Google Chrome [here](https://sites.google.com/a/chromium.org/chromedriver/home).


## Setup

Run `./download-data.sh`. Then, download `ZIP-COUNTY-FIPS_2018-03.csv` from [data.world](https://data.world/niccolley/us-zipcode-to-county-state). You will need to register an account.

The files `cc-est2018-alldata.csv`, `indiv_header_file.csv`, `itcont.txt`, `zip_code_database.csv`, and `ZIP-COUNTY-FIPS_2018-03.csv` should be in the working directory for this project.


## Data Preparation

First, group and sum our contributions by zip code,

```
./prepare_zipcodes.py
```

This will create `contrib-by-zip.csv`. The script will take some time to run. The code for extrapolating zip codes for incomplete rows is the current bottleneck.

Then, group and sum our contributions by county,

```
./prepare_counties.py
```

This will create `contrib-by-zip.csv`.


## Visualization

To visualize the **total individual contributions per county** run

```
./visual_counties.py
```

This will create the image `indiv-contrib-by-county.png`.