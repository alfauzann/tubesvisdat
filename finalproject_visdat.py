# -*- coding: utf-8 -*-
"""FinalProject_Visdat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bbdQZi-sjLVeWggd5mVnMcZ9PzGIMfr2

# Import data
"""

import pandas as pd
import numpy as np

from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool, GroupFilter,CDSView, DateRangeSlider, CustomJS,Dropdown
from bokeh.layouts import row, column, gridplot, layout
from bokeh.resources import INLINE

from datetime import date

data = pd.read_csv("./data/WHO-COVID-19-global-data.csv", parse_dates=['Date_reported'])
data

data.info()

data = data[["Date_reported", 'Country', 'New_cases', 'Cumulative_cases','New_deaths','Cumulative_deaths']]
data = data.rename(columns={'Date_reported': 'Date'})

output_notebook(resources=INLINE)

DT = (data[(data['Country'] == 'United States of America') | (data['Country'] == 'China') | (data['Country'] == 'Indonesia')]
               .loc[:, ['Date', 'Country', 'New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']]
               .sort_values(['Date']))
DT

DT.info()

# Membuat file yang dioutputkan
output_file('KasusCovid19.html', 
            title='Covid-19 in United States of America, Indonesia and China')

# Mengisolasi data 
it_data2 = DT[DT['Country'] == 'United States of America']
ind_data2 = DT[DT['Country'] == 'China']
ina_data2 = DT[DT['Country'] == 'Indonesia']

# Membuat ColumnDataSource objek untuk setiap team
it_cds2 = ColumnDataSource(it_data2)
ind_cds2 = ColumnDataSource(ind_data2)
ina_cds2 = ColumnDataSource(ina_data2)

# memilih fitur interaktif
select_tools = ['pan', 'reset', 'box_select', 'wheel_zoom','box_zoom']


#membuat date range
date_range_slider = DateRangeSlider(value=(date(2020, 1, 3), date(2022, 6, 10)),
                                    start=date(2020, 1, 3), end=date(2022, 6, 10))
date_range_slider.js_on_change("value", CustomJS(code="""
    console.log('date_range_slider: value=' + this.value, this.toString())
"""))

frames = [ind_data2, it_data2, ina_data2]
datasource = pd.concat(frames)
data_Source = ColumnDataSource(datasource)

# Membuat view untuk setiap data
China_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='China')])

Ina_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='Indonesia')])

USA_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='United States of America')])

common_China_kwargs = {
    'view': China_view,
    'legend_label': 'China'
}
common_Indonesia_kwargs = {
    'view': Ina_view,
    'legend_label': 'Indonesia'
}
common_USA_kwargs = {
    'view': USA_view,
    'legend_label': 'United States of America'
}

# membuat figur/grafik
fig = figure(x_axis_type='datetime',
             plot_height=600, plot_width=800,
             title='Kasus Covid-19 di China, United States of America dan Indonesia (Klik label untuk melihat)',
             x_axis_label='Date', y_axis_label='New Cases',
             toolbar_location='right', tools=select_tools)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='red',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_China_kwargs)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='blue',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_USA_kwargs)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='green',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_Indonesia_kwargs)


fig.add_tools(HoverTool(tooltips=[('Date', '@Date{%F}'),  ('Country', '@Country'),
            ('New Cases','@New_cases'),
            ('Cumulative Cases', '@Cumulative_cases'),
            ('New Deaths', '@New_deaths'),
            ('Cumulative Deaths','@Cumulative_deaths')],
          formatters={'@Date': 'datetime'}))

fig.legend.location = 'top_left'

#fitur menghide label
fig.legend.click_policy = 'mute'

# memunculkan slider
date_range_slider.js_link("value", fig.x_range, "start", attr_selector=0)
date_range_slider.js_link("value", fig.x_range, "end", attr_selector=1)

# show grafik 
layout = layout([fig], [date_range_slider])
show(layout)
curdoc().add_root(layout)