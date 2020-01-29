#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

DATA_PATH = 'percap-by-county.csv'
OUTPUT_PATH = 'cnt_vs_amt_percap.png'

if __name__ == '__main__':
    alt.renderers.enable('png')

    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'county_id': 'id'}, inplace=True)

    chart = alt.Chart(df).mark_point(size=200).encode(
        x=alt.X('cnt_per_cap:Q', title='Number of Contributions Per Capita'),
        y=alt.Y('amt_per_cap:Q', title='Contribution Per Capita ($)'),
        color=alt.Color('urban_rural', legend=alt.Legend(title=''))
    ).properties(
        title='',
        width=2000 * 3/4,
        height=1200 * 3/4
    ).configure_title(
        fontSize=50
    ).configure_axis(
        titleFontSize=40,
        labelFontSize=30
    ).configure_legend(
        titleFontSize=40,
        labelFontSize=36
    )

    print('Saving chart to {}...'.format(OUTPUT_PATH))
    chart.save(OUTPUT_PATH)

    print('Done')
