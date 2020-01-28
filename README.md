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

Download campaign contribution data from the Federal Election Commission and unzip it,

```
wget https://www.fec.gov/files/bulk-downloads/data_dictionaries/indiv_header_file.csv
wget https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip
unzip indiv20.zip
```

Now download and unzip the ZIP code data,

```
wget https://simplemaps.com/static/data/us-zips/1.7/basic/simplemaps_uszips_basicv1.7.zip
unzip simplemaps_uszips_basicv1.7.zip
```

Finally, download `ZIP-COUNTY-FIPS_2018-03.csv` from [data.world](https://data.world/niccolley/us-zipcode-to-county-state)

The files `indiv_header_file.csv`, `itcont.txt`, `zip_code_database.csv`, and `ZIP-COUNTY-FIPS_2018-03.csv` should be in the working directory for this project.


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