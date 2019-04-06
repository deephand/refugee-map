import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import time
import os
from prepare_df import prepare_df


def prepare_layout(year: str,
                   longitude_range: list = [-10, 70],
                   latitude_range: list = [20, 70]) -> go.Layout:
    layout = go.Layout(
        title=go.layout.Title(
            text='Refugees per 1000 inhabitants in {}'.format(year),
            font=dict(
                size=32
            )
        ),
        geo=go.layout.Geo(
            showframe=False,
            projection=go.layout.geo.Projection(
                type='natural earth'
            ),
            scope='world',
            showsubunits=True,
            resolution=50,
            lonaxis=go.layout.geo.Lonaxis(
                showgrid=False,
                range=longitude_range
            ),
            lataxis=go.layout.geo.Lataxis(
                showgrid=False,
                range=latitude_range
            ),
            showland=True,
            landcolor="rgb(15,105,105)"
        ),
        margin=go.layout.Margin(
            l=5,
            r=5,
            b=1,
            t=55,
            pad=1
        ),
        annotations=[go.layout.Annotation(
            x=0.13,
            y=0.002,
            xref='paper',
            yref='paper',
            text='Source: World Bank. Prepared by: deephand',
            font=dict(
                color='rgb(220,220,220)'
            ),
            showarrow=False
        )]
    )
    return layout


def make_sub_data(df: pd.DataFrame, year: str,
                  val_range: list, color_range: list,
                  i: int, N: int) -> dict:
    # check if empty
    choropleth = dict(
        type='choropleth',
        locations=df['Country Code'],
        z=df[year],
        text=df['Country Name'],
        colorscale=[[0, color_range[0]], [1, color_range[1]]],
        zmin=val_range[0],
        zmax=val_range[1],
        colorbar=dict(
            x=0.9,
            y=i/float(N) + 0.12,
            ypad=0,
            len=1/float(N),
            tick0=val_range[0],
            dtick=val_range[1]-val_range[0]
        )
    )
    # print(year, len(df))
    if df.size == 0:
        # print(df)
        choropleth['locations'] = ['NOP']
        choropleth['z'] = [0]
    return choropleth


def prepare_data(df: pd.DataFrame, year: str,
                 seps: list = [0, 0.5, 1, 5, 10, 50,
                               100, 500, 1000],
                 colors: list = ["rgb(247,244,249)", "rgb(231,225,239)",
                                 "rgb(212,185,218)", "rgb(201,148,199)",
                                 "rgb(223,101,176)", "rgb(231,41,138)",
                                 "rgb(206,18,86)", "rgb(152,0,67)",
                                 "rgb(103,0,31)"]) -> list:
    """
    len(seps) == len(colors)
    """

    if(len(seps) != len(colors)):
        print('Seps and colors should be the same length.')
        return None

    all_data = []

    for i in range(len(seps) - 1):
        sub_range = [seps[i], seps[i + 1]]
        color_range = [colors[i], colors[i + 1]]
        cond_lower = df[year] >= seps[i]
        cond_higher = df[year] < seps[i + 1]
        sub_df = df[cond_lower & cond_higher]

        sub_data = make_sub_data(sub_df, year,
                                 sub_range, color_range, i, len(seps))
        all_data.append(sub_data)

    return all_data


def plot_years(df: pd.DataFrame, years: list,
               saveImg: bool = False, wait: int = 10) -> None:
    if saveImg:
        pio.orca.config.executable = '/Applications/orca.app/Contents/MacOS/orca'
        try:
            os.mkdir('images')
        except Exception as e:
            print('Folder exists, rewriting.')
    for year in years:
        selector = str(year)
        data = prepare_data(df, selector)
        layout = prepare_layout(selector)
        fig = go.Figure(data=data, layout=layout)
        if saveImg:
            pio.write_image(fig, 'images/{}.jpg'.format(selector),
                            width=1920, height=1080)
        else:
            py.plot(fig, filename='refugees.html')
            time.sleep(wait)
        print(year)


if __name__ == '__main__':
    years = range(1990, 2018)
    # years = [2000,2017]
    per_x_people = 1000
    ratio = prepare_df(years=years)
    ratio[[str(year) for year in years]] *= per_x_people
    plot_years(ratio, years, saveImg=False, wait=2)
