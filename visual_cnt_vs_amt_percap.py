#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

DATA_PATH = 'percap-by-county.csv'
OUTPUT_PATH = '8-raw.png'

if __name__ == '__main__':
    alt.renderers.enable('png')

    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'county_id': 'id'}, inplace=True)

    scatter = alt.Chart(df).mark_point(
        size=200, clip=True, color='lightgrey'
    ).encode(
        x=alt.X('cnt_per_cap:Q', scale=alt.Scale(domain=(0.0, 0.20)), title='Number of Contributions Per Capita'),
        y=alt.Y('amt_per_cap:Q', scale=alt.Scale(domain=(0.0, 60.0)), title='Contribution Amount Per Capita ($)'),
    )

    lines = scatter.transform_regression(
        'cnt_per_cap', 'amt_per_cap', groupby=['urban_rural']
    ).mark_line(size=4, clip=True).encode(
        x=alt.X('cnt_per_cap:Q', scale=alt.Scale(domain=(0.0, 0.20)), title='Number of Contributions Per Capita'),
        y=alt.Y('amt_per_cap:Q', scale=alt.Scale(domain=(0.0, 60.0)), title='Contribution Amount Per Capita ($)'),
    )

    chart = (scatter + lines).properties(
        title='The More Often People Contribute, The Higher They Contribute',
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
