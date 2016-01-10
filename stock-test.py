from bokeh.plotting import Figure
from bokeh.models.widgets import VBoxForm, TextInput
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.glyphs import Quad
import pandas as pd
from bokeh.io import curdoc
import time

AAPL = pd.read_csv(
        "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=1980&d=0&e=1&f=2015",
        parse_dates=['Date']
    )
    
def ConvertToEpoch(time_data):
    return time.mktime(time_data.timetuple()) * 1000

def update_data(attrname,old,new):
    start_x = float(text_start_x.value)
    end_x=float(text_end_x.value)   
    NewestDate_i=0
    OldestDate_i=len(AAPL['Date'])
    for i in range(0,len(AAPL['Date'])):
        curr_time=ConvertToEpoch(AAPL['Date'][i])
        if curr_time>start_x and curr_time<end_x:
            if NewestDate_i==0:
                NewestDate_i=i
            OldestDate_i=i
    new_step=int((OldestDate_i-NewestDate_i)/PLOT_WIDTH)
    NewestDate_i=NewestDate_i+new_step-1
    if OldestDate_i<new_step:
        OldestDate_i=0
    else:
        OldestDate_i=OldestDate_i-new_step
    if new_step<1: new_step=1
    plot_zoomed.y_range.start=min(source_zoomed.data['y'])
    plot_zoomed.y_range.end=max(source_zoomed.data['y'])
    source_zoomed.data=dict(x=AAPL['Date'][NewestDate_i:OldestDate_i:new_step], y=AAPL['Close'][NewestDate_i:OldestDate_i:new_step]) 
    sourceQuad.data = dict(left=[start_x],top=[Max_Y],right=[end_x],bottom=[Min_Y])



def print_value(attrname,old,new):
    update_data()


LastElement=len(AAPL['Date'])-1
source_small = ColumnDataSource(data=dict(x=AAPL['Date'][0:LastElement-1:10], y=AAPL['Close'][0:LastElement-1:10]))
source_zoomed = ColumnDataSource(data=dict(x=AAPL['Date'][0:LastElement-1:10], y=AAPL['Close'][0:LastElement-1:10]))
Min_Y=int(min(source_small.data['y'])-10)
Max_Y=int(max(source_small.data['y'])+10)
#Range_Y=Range1d(Min_Y,Max_Y)

PLOT_WIDTH=500
sourceQuad = ColumnDataSource(dict(left=[min(source_small.data['x'])],top=[Max_Y],right=[max(source_small.data['x'])],bottom=[Min_Y]))

toolset = "box_zoom,resize,pan,reset,save,xwheel_zoom"
plot_zoomed = Figure(plot_width=1000, plot_height=500, x_axis_type="datetime",tools=toolset, lod_factor=100,lod_interval=1000)
plot_zoomed.line('x', 'y',source=source_zoomed, color='navy', alpha=0.5)
plot = Figure(plot_width=PLOT_WIDTH, plot_height=250, x_axis_type="datetime",toolbar_location=None,lod_factor=100,lod_interval=1000)
plot.line('x', 'y',source=source_small, color='navy', alpha=0.5)
plot.y_range.start=Min_Y
plot.y_range.end=Max_Y
glyph = Quad(left="left", right="right", top="top", bottom="bottom", fill_color="#b3de69", fill_alpha=0.1)
plot.add_glyph(sourceQuad, glyph)

RangeStartX=0
RangeEndX=1
text_start_x = TextInput(title="X range start", name='x_range_start', value="0")
text_end_x = TextInput(title="X range end", name='x_range_end', value="1")
text_start_x.on_change('value', update_data)
text_end_x.on_change('value', update_data)

toolset = "box_zoom,resize,pan,reset,save,x_wheel_zoom"

plot_zoomed.x_range.callback = CustomJS(args=dict(xrange=plot_zoomed.x_range,start_x=text_start_x,end_x=text_end_x),code="""
var start = xrange.get("start");
var end = xrange.get("end");
start_x.set("value",start.toString());
end_x.set("value",end.toString());
start_x.trigger('change');
end_x.trigger('change');
""")

curdoc().add_root(VBoxForm(children=[plot_zoomed,plot], width=1000))
