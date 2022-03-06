import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc

data = pd.read_csv('marvel_clean.csv')
open_week_us = data.groupby(['Distributor'])['OpeningWeekendNorthAmerica'].mean()

chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'For Marvel Movies distributed between 1986-2022'
    },
    subtitle: {
        text: 'Data scarped from: https://en.wikipedia.org/wiki/List_of_films_based_on_Marvel_Comics_publications'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Distributors'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Revenue Collected'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '$ {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Distributions:',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a = wp, text = 'Average Revenue Collected by each Distributor on the Opening Weekend in USA', classes = 'text-h3 text-center q-pa-md')

    hc = jp.HighCharts(a = wp, options = chart_def)
    hc.options.xAxis.categories = list(open_week_us.index)
    hc.options.series[0].data = list(open_week_us.round(2))

    return wp

jp.justpy(app)
