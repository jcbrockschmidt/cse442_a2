#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

DATA_PATH = 'percap-by-county.csv'
OUTPUT_PATH = '6-raw.png'

if __name__ == '__main__':
    alt.renderers.enable('png')

    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'county_id': 'id'}, inplace=True)

    scatter = alt.Chart(df).mark_point(size=200, clip=True).encode(
        x=alt.X('pop:Q', scale=alt.Scale(type='log'), title='County Population'),
        y=alt.Y('cnt_per_cap:Q', title='Number of Contributions Per Capita', scale=alt.Scale(domain=(0, 0.3))),
        color=alt.Color('urban_rural', legend=alt.Legend(title=''), sort=['ua', 'uc', 'rural'])
    )

    lines = scatter.transform_regression(
        'pop', 'cnt_per_cap', groupby=['urban_rural']
    ).mark_line(size=8, clip=True).encode(
        x=alt.X('pop:Q', scale=alt.Scale(type='log'), title='County Population'),
        y=alt.Y('cnt_per_cap:Q', title='Number of Contributions Per Capita', scale=alt.Scale(domain=(0, 0.3)))
    )

    line_all = scatter.transform_regression(
        'pop', 'cnt_per_cap', method='linear'
    ).mark_line(size=6, clip=True).encode(
        x=alt.X('pop:Q', scale=alt.Scale(type='log'), title='County Population'),
        y=alt.Y('cnt_per_cap:Q', title='Number of Contributions Per Capita', scale=alt.Scale(domain=(0, 0.3)))
    )

    chart = (scatter + lines + line_all).properties(
        title='Correlating Population Size and Number of Contributions',
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
