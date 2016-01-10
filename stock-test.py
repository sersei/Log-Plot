import time

import numpy as np

from bokeh.io import curdoc
from bokeh.models import HoverTool, HBox, VBox, Slider, Toggle
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.sampledata.us_states import data as states
from bokeh.palettes import Purples9

states = {
    code: state for code, state in states.items() if
    code not in ['HI', 'AK']
}

def gen_initial_rate(y):
    return min(
        np.random.choice([15, 40]) + np.random.uniform(-10, 10),
        100
    )

state_xs = [state['lons'] for state in states.values()]
state_ys = [state['lats'] for state in states.values()]
colors = Purples9[::-1]

names = [state['name'] for state in states.values()]
initial_rates = [gen_initial_rate(1) for _ in states.values()]
state_colors = [colors[int(rate / 20)] for rate in initial_rates]

source = ColumnDataSource(data=dict(
    x=state_xs,
    y=state_ys,
    color=state_colors,
    name=names,
    rate=initial_rates
))

TOOLS=['hover']

p = figure(title='Algorithms Deployed, Iteration 0', tools=TOOLS,
           plot_width=1440, plot_height=810)
patches = p.patches('x', 'y', source=source,
                    fill_color='color', fill_alpha=0.85,
                    line_color='white', line_width=0.5)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.yaxis.axis_line_color = None
p.xaxis.axis_line_color = None

hover = p.select_one(HoverTool)
hover.point_policy = 'follow_mouse'
hover.tooltips = [
    ('Name', '@name'),
    ('Score', '@rate')
]
counter = 0
def run(new):
    global p, patches, colors, counter

    for _ in range(slider.value):
        counter += 1
        data = patches.data_source.data.copy()
        rates = np.random.uniform(0, 100, size=100).tolist()
        color = [colors[2 + int(rate / 16.667)] for rate in rates]

        p.title = 'Algorithms Deployed, Iteration: {}'.format(counter)
        source.data['rate'] = rates
        source.data['color'] = color
        time.sleep(5)

toggle = Toggle(label='START')
toggle.on_click(run)

slider = Slider(name='N iterations to advance',
                title='N iterations to advance',
                start=5,
                end=10000,
                step=5,
                value=500)

# set up layout
toggler = HBox(toggle)
inputs = VBox(toggler, slider)

# add to document
curdoc().add_root(HBox(inputs))
