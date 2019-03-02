'''Contains the methods to generate a visualization from data. Employs the
Bokeh library to connect Python to Javascript.

'''
from bokeh.embed import components, file_html
#
# TODO Bokeh has made stuff obsolete
#
#from bokeh.charts import Bar, BoxPlot
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Range1d, HoverTool
from bokeh.resources import Resources

import pandas as pd
import numpy as np

class Visualizer:
    '''The Visualizer class accepts data of a well-defined format along with
    data semantics, and generates a Javascript visualization. The
    initialization defines key attributes and general styling that applies
    to any type of data visualizations. The methods accept the data and any
    particular styling specifications. The form of the output depends on which
    method is called following the visualization method.

    '''
    def stacked_bars(self, df, x_axis, y_axis, stack, title=None):
        '''Generate stacked bars visualization.

        Args:
            df (pandas Series): Data to plot. This should be shaped as a
                                MultiIndex Pandas Series, where each
                                level of index is named, and there is one 
                                column of data, also with a name.
            x_axis (string): Name of index type to define the bars on the
                             horizontal axis. Each unique index of that index
                             type becomes a bar.
            y_axis (string): What values to define stack size of bars. This
                             should always equal the name of the single column.
            stack (string): Name of the index type to define the categories of
                            data to stack. Each unique index of that index type
                            becomes a segment of each bar.
            title (string, optional): Title to add at top of data visualization.

        Returns: None

        '''
        # Re-shape data as required by Bokeh
        df_columnwise = df.reset_index()
        df_columnwise[y_axis] = df_columnwise[y_axis].astype(float)

        # Create a stacked bar
        print (df_columnwise)
        raise RuntimeError
#        p = Bar(df_columnwise, label=x_axis, stack=stack, values=y_axis,
#                title=title, legend=self.legend, **self.plot_defaults)

        self.graph_object = p

    def scatter_plot(self, df, x_axis, y_axis, level_name, x_range=None, y_range=None,
                     title=None, size=10.0, color='#0000ff', alpha=1.0):
        '''Generate scatter plot.

        Args:
            df (pandas Series): Data to plot. This should be shaped as a
                                MultiIndex Pandas Series, where each level of
                                index is named, and there is one column of
                                data, also with a name.
            x_axis (string): Name of index of type defined by level_name to be
                             used to define horizontal coordinates.
            y_axis (string): Name of index of type defined by level_name to be
                             used to define vertical coordinates.
            level_name (string): Name of index type from which to collect the
                                 horizontal and vertical coordinate data.
            x_range (tuple, optional): Two integers to define lower and upper
                                       bound of horizontal axis; if None the
                                       min and max of data is used.
            y_range (tuple, optional): Two integers to define lower and upper
                                       bound of vertical axis; if None the
                                       min and max of data is used.
            title (string, optional): Title to add at top of data visualization.
            size (float, optional): Size of marker.
            color (string, optional): Color of marker.
            alpha (float, optional): Transparency of marker.

        Returns: None

        '''
        df_x = df.xs(x_axis, level=level_name)
        df_y = df.xs(y_axis, level=level_name)
        index_ids = df_x.index.values
        index_ids_string = ['-'.join(point_name) for point_name in index_ids]
        x_data = df_x.values
        y_data = df_y.values

        # In order to enable Hover Tool, the data is given a descriptor
        source = ColumnDataSource(data=dict(
                                  x = x_data, y = y_data,
                                  desc = index_ids_string,))
        hover = HoverTool(tooltips=[('(x,y)','(@x, @y)'),
                                   ('desc','@desc')])

        p = figure(tools=[hover], **self.plot_defaults)
        p.circle('x', 'y', size=size, source=source, color=color,
                 alpha=alpha)
        
        # Force certain range on horizontal and vertical axes.
        if not x_range is None:
            p.x_range = Range1d(*x_range) 
        if not y_range is None:
            p.y_range = Range1d(*y_range) 

        self.graph_object = p

    def box_plot(self, df, values, label, outliers=True, title=None):
        '''Generate box plots.

        Args:
            df (pandas Series): Data to plot. This should be shaped as a
                                MultiIndex Pandas Series, where each
                                level of index is named, and there is one 
                                column of data, also with a name.
            values (string): Name of data to obtain data from in order to build
                             box plot. Should be numeric.
            label (string): Name of column to obtain category names from to be
                            displayed on horizontal axis for each box plot.
            outliers (bool, options): Set to True if outliers are to be shown
                            as individual dots in box plot. Set to False in
                            case outliers are merged into the plot.
            title (string, optional): Title to add at top of data visualization.

        '''
        # Re-shape data as required by Bokeh
        df_columnwise = df.reset_index()
        df_columnwise[values] = df_columnwise[values].astype(float)

        # Make the box plot along with styling settings
        print (df_columnwise)
        raise RuntimeError
#        p = BoxPlot(df_columnwise, values=values, label=label,
#                    title=title, outliers=outliers, legend=self.legend, 
#                    **self.plot_defaults)

        self.graph_object = p

    def spider_plot(self, df, dims, same_level_norm=False, common_range=None,
                    alpha=0.6):
        '''Generate spider plot.

        Args:
            df (pandas Series): Data to plot. This should be shaped as a
                                MultiIndex Pandas Series, where each
                                level of index is named, and there is one 
                                column of data, also with a name.
            dims (string): Name of index type that defines dimensions of data.
            save_level_norm (bool, optional): If True, make each leg in plot
                                   bounded by the same (global) maximum and minimum.
            common_range (tuple, optional): A tuple of the minimum and maximum
                                   to bound all legs in plot by; must include
                                   all data. 
            alpha (float, optional): Transparency of web lines.

        Returns: None

        '''
        # Determine number of dimensions, and hence leg distribution 
        if not dims in df.index.names:
            raise KeyError('Dimension with name %s not found in data' %(dims))
        else:
            levels = df.index.levels[df.index.names.index(dims)]
            n_legs = len(levels)
        angles = [x * 2.0 * np.pi / len(levels) for x in range(0, n_legs)]

        # Compute ranges of each bar
        axis_ranges = []
        level_data = []
        for level in levels:
            df_level = df.xs(level, level=dims)
            level_max = df_level.max()
            level_min = df_level.min()
            axis_ranges.append((level_min, level_max))
            level_data.append(df_level)
        n_webs = len(level_data[0])

        max_of_max = max([axis_range[1] for axis_range in axis_ranges])
        min_of_min = min([axis_range[0] for axis_range in axis_ranges])
        if same_level_norm:
            axis_ranges = [(min_of_min, max_of_max)] * n_legs

        if not common_range is None:
            axis_ranges_new = []
            for axis_range in axis_ranges:
                if axis_range[0] < common_range[0] or \
                   axis_range[1] > common_range[1]:
                    raise ValueError('Common range for spider plot does ' + \
                          'not contain data of range ' + \
                          '%s to %s' %(str(axis_range[0]), str(axis_range[1])))
                else:
                    axis_range_new = common_range
                axis_ranges_new.append(axis_range_new)
            axis_ranges = axis_ranges_new

        # Translate data into xy-coordinates for plot
        point_coords = []
        for data, axis_range, angle in zip(level_data, axis_ranges, angles):
            line_coords_x = []
            line_coords_y = []
            for data_point in data:
                radial = (data_point - axis_range[0]) / (axis_range[1] - axis_range[0])
                x = radial * np.sin(angle)
                y = radial * np.cos(angle)
                line_coords_x.append(x)
                line_coords_y.append(y)
            point_coords.append([line_coords_x, line_coords_y])

        # Resort the xy-coordinates according to convention by plotting program
        data_to_plot = {}
        for xy in [0, 1]:
            line_data = []
            for line in range(0, n_webs):
                points = list(range(0, n_legs)) + [0]
                point_data = []
                for point in points:
                    point_data.append(point_coords[point][xy][line])
                line_data.append(point_data)
            data_to_plot[xy] = line_data

        # Create axis line
        base_line = [0.0, 1.1 * max_of_max]
        axis_to_plot = {}
        for angle in angles:
            x = base_line[0] * np.cos(angle) + base_line[1] * np.sin(angle)
            y = base_line[0] * np.sin(angle) + base_line[1] * np.cos(angle)
            coord_x = axis_to_plot.setdefault(0, [])
            coord_y = axis_to_plot.setdefault(1, [])
            coord_x.append([0.0, x])
            coord_y.append([0.0, y])
            axis_to_plot[0] = coord_x
            axis_to_plot[1] = coord_y

        p = figure(**self.plot_defaults)
        # TODO: Make color a property by cluster list as set from input
        p.multi_line(data_to_plot[0], data_to_plot[1], alpha=alpha)
        p.multi_line(axis_to_plot[0], axis_to_plot[1], color='black',
                     line_width=2.0)

        # Hide grid and axes
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.axis.visible = False

        self.graph_object = p 

    def _make_html(self):
        '''Generate html string object with the javascript data visualization
        embedded.

        Args: None

        Returns:
            out_data (tuple): tuple of lists of strings, where the string is
                              the HTML data, including the embedded Javascript
                              data visualization, as well as the data semantic
                              notation '.html'.

        '''
        html = file_html(self.graph_object, self.bokeh_resource)
        data = [html]
        semantics = ['.html']

        return (data, semantics)

    def _make_components(self):
        '''Generate Javascript string object of the data visualization, along
        with a HTML snippet required to render to Javascript if embedded in a
        HTML file.

        Args: None

        Returns:
            out_data (tuple): tuple of lists of strings, where the string is
                              the Javascript code of the data visualization, as
                              well as the HTML snippet. The second element of
                              tuple contains data semantic notations '.js' and
                              '.html_div'.

        '''
        script, div = components(self.graph_object)
        data = [script, div]
        semantics = ['.js', '.html_div']

        return (data, semantics)

    def get_descr(self, method_key):
        '''Obtain description for a given visualization method. If no
        description exists for the given key, an empty string is returned.

        Args:
            method_key (string): Name of visualization method.

        Returns:
            descr (string): Description text for the visualization method.

        '''
        try:
            descr = self._viz_method_descr[method_key]
        except KeyError:
            descr = '' 

        return descr

    def get_output(self):
        '''Method to return output data for the visualization. The type of
        output data is set during initialization.

        Args:
            None

        Returns:
            out_data (tuple): tuple of lists of strings, where each string is
                              the specified type of data, and the two elements
                              of the tuple are the actual data and a simple
                              descriptor of the type of string data.

        Raises:
            AttributeError: In case either the method is called prior to a
                            method for Javascript generation, or an invalid
                            output format is requested.

        '''
        if self.graph_object is None:
            raise AttributeError('There is no visualization data to output')

        if self.output_format == 'html':
            ret = self._make_html()
        elif self.output_format == 'javascript':
            ret = self._make_components()
        else:
            raise AttributeError('No valid output format defined')

        return ret

    def write_output(self, path_dir, namespace):
        '''Write output files to set directory and namespace

        Args:
            path_dir (string): Path to directory into which to place files.
            namespace (string): Root string of name of files. 

        Returns: None

        '''
        if path_dir[-1] == '/':
            path = path_dir + namespace
        else:
            path = path_dir + '/' + namespace

        data, semantics = self.get_output()
        for point, semantic in zip(data, semantics):
            with open(path + semantic, 'w') as fout:
                fout.write(point)

    def __init__(self, legend='top_right', write_output_format='javascript',
                 background_color='#ffffff'):
        '''Bla bla

        '''
        self.graph_object = None

        self.output_format = write_output_format
        self.legend = legend
        self.bokeh_resource = Resources(mode='cdn')
        self.plot_defaults = {'background_fill_color':background_color}

        self._viz_method_descr = \
        {'scatter_plot' : 'abc',
         'spider_plot' : '',
         'stacked_bars' : '',
         'box_plot' : ''}
