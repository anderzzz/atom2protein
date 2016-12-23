'''Bla bla

'''
from bokeh.charts import Bar, output_file, show 
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Range1d, HoverTool
import pandas as pd

class Visualizer:
    '''Bla bla

    '''
    def stacked_bars(self, df, x_axis, y_axis, stack, title=None):
        '''Bla bla

        '''
        df_columnwise = df.reset_index()
        df_columnwise[y_axis] = df_columnwise[y_axis].astype(float)
        p = Bar(df_columnwise, label=x_axis, stack=stack, values=y_axis, title=title)
        self.graph_object = p

    def scatter_plot(self, df, x_axis, y_axis, level_name, x_range=None, y_range=None,
                     title=None):
        '''Bla bla

        '''
        df_x = df.xs(x_axis, level=level_name)
        df_y = df.xs(y_axis, level=level_name)
        index_ids = df_x.index.values
        index_ids_string = ['-'.join(point_name) for point_name in index_ids]
        x_data = df_x.values
        y_data = df_y.values

        source = ColumnDataSource(data=dict(
                                  x = x_data, y = y_data,
                                  desc = index_ids_string,))
        hover = HoverTool(tooltips=[('(x,y)','(@x, @y)'),
                                   ('desc','@desc')])
        p = figure(tools=[hover])
        p.circle('x', 'y', size=10, source=source)
        self.graph_object = p

    def make_html(self, fileout_path):
        '''Bla bla

        '''
        output_file(fileout_path)
        show(self.graph_object)

    def __init__(self, legend='top_right'):
        '''Bla bla

        '''
        self.legend = legend

        self.graph_object = None
