#!/usr/bin/env python3

import pandas as pd

POP_PATH = 'cc-est2018-alldata.csv'
CONT_PATH = 'contrib-by-county.csv'
OUTPUT_PATH = 'percap-by-county.csv'

if __name__ == '__main__':
    print('Loading data...')
    pop = pd.read_csv(POP_PATH, encoding='ISO-8859-1')
    pop = pop[['STATE', 'COUNTY', 'YEAR', 'TOT_POP']]
    cont = pd.read_csv(CONT_PATH)

    print('Preparing data...')
    # Get population statistics from July 2018
    pop = pop.loc[pop['YEAR'] == 11].drop(columns=['YEAR'])

    # Combine state and county FIPS code into single identifier
    pop['county_id'] = pop['STATE'] * 1000 + pop['COUNTY']
    pop.drop(columns=['STATE', 'COUNTY'], inplace=True)

    # Sum together population from all age groups, grouped by county.
    pop = pop.groupby(['county_id']).sum().reset_index()
    pop.rename(columns={'TOT_POP': 'pop'}, inplace=True)

    # Get per-capita individual contributions statistics
    cont = pd.merge(cont, pop, on='county_id', how='outer')
    # Excludes US territories
    cont.dropna(inplace=True)
    cont['amt_per_cap'] = cont['amt'] / cont['pop']
    cont['cnt_per_cap'] = cont['cont_cnt'] / cont['pop']
    cont['pop'] = cont['pop'].astype(int)

    # Add label for Urbanized Areas (UAs), Urban Clusters (UCs), and rural areas.
    # We use the definitions of these given by the US Census Bureau.
    #  * Urbanized Areas (UAs) - [50000, ...)
    #  * Urban Clusters (UCs) - [2500, 50000)
    #  * Rural - (.., 2500)
    cont.loc[cont['pop'] >= 50000, 'urban_rural'] = 'ua'
    cont.loc[(cont['pop'] >= 2500) & (cont['pop'] < 50000), 'urban_rural'] = 'uc'
    cont.loc[cont['pop'] < 2500, 'urban_rural'] = 'rural'

    print('Saving data to {}...'.format(OUTPUT_PATH))
    cont.to_csv(OUTPUT_PATH, index=False)
