#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

DATA_PATH = 'contrib-by-county.csv'
OUTPUT_PATH = '1-raw.png'

if __name__ == '__main__':
    alt.renderers.enable('png')

    counties = alt.topo_feature(data.us_10m.url, 'counties')

    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'county_id': 'id'}, inplace=True)

    # Apply log scaling to the total contribution amount.
    df['amt'] = df['amt'].apply(lambda x: np.log10(x))

    chart = alt.Chart(counties).mark_geoshape().encode(
        #color=alt.Color('amt:Q', scale=alt.Scale(type='log', scheme='greenblue'))
        color=alt.Color(
            'amt:Q',
            scale=alt.Scale(scheme='greenblue'),
            legend=alt.Legend(title='Log of Amount ($)', tickCount=6)
        )
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df, 'id', ['amt'])
    ).project(
        type='albersUsa'
    ).properties(
        title='Total Monetary Contributions by County',
        width=2000,
        height=1200
    ).configure_legend(
        gradientLength=600,
        gradientThickness=50,
        titleFontSize=30,
        labelFontSize=24
    ).configure_title(
        fontSize=50
    )

    print('Saving chart to {}...'.format(OUTPUT_PATH))
    chart.save(OUTPUT_PATH)

    print('Done')
