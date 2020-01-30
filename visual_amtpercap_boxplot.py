#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd

DATA_PATH = 'percap-by-county.csv'
OUTPUT_PATH = '5-raw.png'

if __name__ == '__main__':
    alt.renderers.enable('png')

    df = pd.read_csv(DATA_PATH)
    df.rename(columns={'county_id': 'id'}, inplace=True)

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X('urban_rural:N', title='', sort=['ua', 'uc', 'rural']),
        y=alt.Y('mean(amt_per_cap):Q', title='Mean Monetary Contribution Per Capita ($)'),
        color=alt.Color('urban_rural:N', legend=None, sort=['ua', 'uc', 'rural'])
    )

    error_bars = alt.Chart().mark_errorbar(extent='ci').encode(
        x=alt.X('urban_rural:N', sort=['ua', 'uc', 'rural']),
        y=alt.Y('mean(amt_per_cap):Q', title='Mean Monetary Contribution Per Capita ($)')
    )

    chart = alt.layer(bars, error_bars, data=df).encode(
        x=alt.X('urban_rural:N', title='', sort=['ua', 'uc', 'rural'])
    ).properties(
        title='People Contribute More Money Per Contribution in More Rural Areas',
        width=250,
        height=600
    ).configure_title(
        fontSize=32
    ).configure_axis(
        titleFontSize=20,
        labelFontSize=16
    ).configure_legend(
        titleFontSize=20,
        labelFontSize=16
    )

    print('Saving chart to {}...'.format(OUTPUT_PATH))
    chart.save(OUTPUT_PATH)

    print('Done')
