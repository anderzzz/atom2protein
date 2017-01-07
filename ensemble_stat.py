'''Bla bla

'''
from visualizers import Visualizer
from summaries import Entry

import inspect
import pandas as pd 

class HowToViz:
    '''Bla bla

    '''
    def add_howto(self, data_entry, method_name, kwargs_dict):
        '''Bla bla

        '''
        if not method_name in self.available_viz_methods:
            raise KeyError('The Visualizer class does not contain a method ' + \
                           'called %s' %(method_name))

        list_of_viz = self.container.setdefault(data_entry, []) 
        list_of_viz.append((method_name, kwargs_dict))
        self.container[data_entry] = list_of_viz

    def __getitem__(self, key):
        '''Bla bla

        '''
        return self.container[key]

    def __init__(self):
        '''Bla bla

        '''
        self.container = {}
        
        self.available_viz_methods = set([name for name, method in
                                     inspect.getmembers(Visualizer,
                                     predicate=inspect.isfunction)])

class EnsembleStat:
    '''Bla bla

    '''
    def _get_entries(self, summa, attrib_collector):
        '''Bla bla

        '''
        if attrib_collector is None:
            attribs = [x for x in dir(summa) if x[0] != '_']
        else:
            attribs = attrib_collector

        for attrib in attribs:
            whatwegot = getattr(summa, attrib)
            if isinstance(whatwegot, Entry):
                yield whatwegot

    def add_entries(self, sum_iterator, attrib=None):
        '''Bla bla

        '''
        collector = [] 
        for data_label, summary_data in sum_iterator.items():
            for entry in self._get_entries(summary_data, attrib): 
                df = entry.unpack_value()
                names = ['id'] + df.index.names
                extended_index = [(data_label, ) + ind for ind in df.index]
                df.index = pd.MultiIndex.from_tuples(extended_index, names=names)
                collector.append(df)

        return pd.concat(collector)

    def _get_summary_subset(self, label_set):
        '''Bla bla

        '''
        c = []
        for s in self.summaries:
            if s.get_label() in label_set:
                c.append(s)
        if len(c) == 0:
            raise KeyError('No data summaries with requested labels exist')

        return c

    def visualize_individual(self, label_set=None):
        '''Bla bla

        '''
        if label_set is None:
            collector = self.summaries
        else:
            collector = self._get_summary_subset(label_set)

        for summary in collector:
            for xx in summary.get_entries():
                viz = Visualizer(write_output_format='html')
                print (self.viz_rundata)
                for viz_method, viz_kwargs in self.viz_rundata[xx.key]:
                    getattr(viz, viz_method)(xx.value, **viz_kwargs)
                    print (viz.get_output())
                raise TypeError('dummy')
            


    def __init__(self, iterof_summaries):
        '''Bla bla

        '''
        self.summaries = iterof_summaries

        self.viz_rundata = HowToViz()
        self.viz_rundata.add_howto('Backbone torsions', 'scatter_plot',
                        {'x_axis' : 'phi', 'y_axis' : 'psi', 
                         'level_name': 'property', 
                         'y_range' : (-180.0, 180.0), 
                         'x_range' : (-180.0, 180.0), 'alpha' : 0.5})

