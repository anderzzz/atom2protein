'''Bla bla

'''
from visualizers import Visualizer
from summaries import Entry

from pathlib import Path
import datetime
import sqlite3
import random, string
import inspect
import pandas as pd 

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
            if s.label in label_set:
                c.append(s)
        if len(c) == 0:
            raise KeyError('No data summaries with requested labels exist')

        return c

    def _get_label_iter(self, label_set):
        '''Bla bla

        '''
        if label_set is None:
            collector = self.summaries
        else:
            collector = self._get_summary_subset(label_set)

        return iter(collector)

    def join(self, types, label_set):
        '''Bla bla

        '''
        ids_to_join = list(self._get_label_iter(label_set))
        ret = ids_to_join[0]
        for x in ids_to_join[1:]:
            ret += x

        return ret

    def visualize_individual(self, entry_types, label_set=None):
        '''Bla bla

        '''
        for summary in self._get_label_iter(label_set): 
            for entry_type in entry_types:
                entry = summary[entry_type]
                viz = Visualizer(write_output_format='html')
                for viz_method, viz_kwargs in self.viz_rundata[entry_type]:
                    namespace = self._randomword(15)
                    now = datetime.datetime.now().ctime()
                    getattr(viz, viz_method)(entry.value, **viz_kwargs)
                    viz.write_output(self.path_viz_out, namespace)
                    self._insert_db(summary.label, entry.brief, viz_method, 
                                    self.path_viz_out, namespace, now)

    def visualize_union(self, union_func, entry_types, label_set=None):
        '''Bla bla

        '''
        summary_union = getattr(self, union_func)(entry_types, label_set)
        for entry_type in entry_types:
            entry = summary_union[entry_type] 
            viz = Visualizer(write_output_format='html')
            for viz_method, viz_kwargs in self.viz_rundata[entry_type]:
                namespace = self._randomword(15)
                now = datetime.datetime.now().ctime()
                getattr(viz, viz_method)(entry.value, **viz_kwargs)
                viz.write_output(self.path_viz_out, namespace)
                self._insert_db(summary_union.label, entry.brief, viz_method, 
                                self.path_viz_out, namespace, now)
            
    def __init__(self, iterof_summaries, path_out=None):
        '''Bla bla

        '''
        self.summaries = iterof_summaries
        self.path_viz_out = path_out

        self.db_conn = self._setup_db(path_out + '/viz.db')
        self.viz_rundata = HowToViz()
        self.viz_rundata.add_howto('bb_torsions', 'scatter_plot',
                        {'x_axis' : 'phi', 'y_axis' : 'psi', 
                         'level_name': 'property', 
                         'y_range' : (-180.0, 180.0), 
                         'x_range' : (-180.0, 180.0), 'alpha' : 0.5})
        self.viz_rundata.add_howto('nresidues', 'stacked_bars',
                        {'x_axis' : 'chain', 'y_axis' : 'residue count', 
                         'stack': 'property'}) 
        self.viz_rundata.add_howto('nresidues_polarity', 'stacked_bars',
                        {'x_axis' : 'id', 'y_axis' : 'residue count', 
                         'stack': 'property'}) 

