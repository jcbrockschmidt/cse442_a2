#!/usr/bin/env python3

import pandas as pd

HEADER_PATH = 'indiv_header_file.csv'
DATA_PATH = 'itcont.txt'
ZIP_DATA_PATH = 'zip_code_database.csv'
OUTPUT_PATH = 'contrib-by-zip.csv'

def load_zip_data():
    colnames = ['zip', 'primary_city', 'state', 'county']
    zips = pd.read_csv(ZIP_DATA_PATH)
    zips = zips[colnames]
    zips = zips.rename(columns={
        'primary_city': 'city',
        'state': 'state_id'
    })
    zips['zip'] = zips['zip'].astype(int)
    return zips

if __name__ == '__main__':
    header = pd.read_csv(HEADER_PATH, header=None)
    names = header.values[0]
    name_to_idx = {v: i for i, v in enumerate(names)}
    usecols = [
        name_to_idx['CITY'],
        name_to_idx['STATE'],
        name_to_idx['ZIP_CODE'],
        name_to_idx['TRANSACTION_AMT'],
    ]

    print('Loading data...')
    zips = load_zip_data()
    zips['city'] = zips['city'].str.upper()
    states = zips['state_id'].unique()
    zip_list = zips['zip'].unique()
    df = pd.read_csv(
        DATA_PATH, delimiter='|',
        names=names, usecols=usecols,
    )
    orig = df.copy()

    # Only include numeric transaction amounts
    print('Omitting bad transaction amounts...')
    df['TRANSACTION_AMT'] = pd.to_numeric(df['TRANSACTION_AMT'], downcast='float', errors='coerce')
    good_df = df.loc[df['TRANSACTION_AMT'].notnull()]
    bad_df = df.loc[~df['TRANSACTION_AMT'].notnull()]
    df = good_df

    # We will use this for summary statistics later.
    total_amt = df['TRANSACTION_AMT'].sum()

    # Only include numeric zip codes
    print('Cleaning zip codes...')
    df['ZIP_CODE'] = pd.to_numeric(df['ZIP_CODE'], downcast='integer', errors='coerce')
    good_df = df.loc[df['ZIP_CODE'].notnull()]
    bad_df = pd.concat([bad_df, df.loc[~df['ZIP_CODE'].notnull()]])
    df = good_df
    df['ZIP_CODE'] = df['ZIP_CODE'].astype(int)

    # Trim zip codes to 5 numbers
    df['ZIP_CODE'] = df['ZIP_CODE'].apply(lambda x: int(str(x)[:5]))

    # Remove invalid zip codes
    print('Removing invalid zip codes...')
    good_df = df.loc[df['ZIP_CODE'].isin(zip_list)]
    bad_df = pd.concat([bad_df, df.loc[~df['ZIP_CODE'].isin(zip_list)]])
    df = good_df

    # Try to find zip codes for our bad rows with valid states
    print('Inferring zip codes of bad rows...')
    print('    Looking at rows with states and cities...')
    bad_with_state = bad_df.loc[bad_df['STATE'].isin(states)]
    bad_with_state.reset_index(inplace=True)
    idx = []
    for i, row in bad_with_state.iterrows():
        maybe = zips.loc[(zips['state_id'] == row['STATE']) & (zips['city'] == row['CITY'])]
        if len(maybe.index) == 1:
            idx.append(i)
            bad_with_state['ZIP_CODE'].iloc[i] = int(maybe['zip'].values[0])
        if i % 1000 == 0 and i != 0:
            print('        {}/{} rows analysed...'.format(i, len(bad_with_state.index)))
    good_df = bad_with_state.iloc[idx]
    good_df['ZIP_CODE'] = good_df['ZIP_CODE'].astype(int)
    df = pd.concat([df, good_df], sort=True)

    # Try to find zip codes for our bad rows without valid states
    print('    Looking at rows with just cities...')
    bad_no_state = bad_df.loc[~bad_df['STATE'].isin(states)]
    bad_no_state.reset_index(inplace=True)
    idx = []
    for i, row in bad_no_state.iterrows():
        maybe = zips.loc[zips['city'] == row['CITY']]
        if len(maybe.index) == 1:
            idx.append(i)
            bad_no_state['ZIP_CODE'].iloc[i] = int(maybe['zip'].values[0])
            bad_no_state['STATE'].iloc[i] = maybe['state_id'].values[0]
        if i % 1000 == 0 and i != 0:
            print('        {}/{} rows analysed...'.format(i, len(bad_no_state.index)))
    good_df = bad_no_state.iloc[idx]
    good_df['ZIP_CODE'] = good_df['ZIP_CODE'].astype(int)
    df = pd.concat([df, good_df], sort=True)

    # Sum transactions amounts, grouping by zip code
    total_rows = len(orig.index)
    rows_used = len(df.index)
    df = df.groupby(['ZIP_CODE', 'STATE']).sum().reset_index()
    df.drop(columns=['index'], inplace=True)
    df.rename(columns={
        'ZIP_CODE': 'zip',
        'STATE': 'state_id',
        'TRANSACTION_AMT': 'amt'
    }, inplace=True)

    # Statistics
    row_percent = rows_used / total_rows * 100
    print('{}/{} ({:.2f}%) rows used'.format(rows_used, total_rows, row_percent))
    used_amt = df['amt'].sum()
    amt_percent = used_amt / total_amt * 100
    print('{:.2f}$/{:.2f}$ ({:.2f}%) contributions used'.format(total_amt, used_amt, amt_percent))

    # Output to file
    print('Saving data to {}'.format(OUTPUT_PATH))
    df.to_csv(OUTPUT_PATH, header=True, index=False)
