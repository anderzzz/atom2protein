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

    def _randomword(self, length):
        '''Bla bla

        '''
        return ''.join(random.choice(string.ascii_lowercase +
                                     string.digits) for i in range(length))

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

    def _setup_db(self, out_file_path='vizfiles.db'):
        '''Bla bla

        '''
        conn = sqlite3.connect(out_file_path)
        c = conn.cursor()

        try:
            c.execute("CREATE TABLE ensemble_files " + \
                      "(source_label, summary_label, ensemble_method, " + \
                      "file_path, file_namespace, created_time)") 
            conn.commit()
        except sqlite3.OperationalError:
            pass

        return conn

    def _insert_db(self, primary, secondary, tertiary, path, ns, time):
        '''Bla bla

        '''
        c = self.db_conn.cursor()
        out_tuple = (primary, secondary, tertiary, path, ns, time)
        c.execute("INSERT INTO ensemble_files VALUES " + \
                  "('%s','%s','%s','%s','%s','%s')" %out_tuple)
        self.db_conn.commit()

    def _get_label_iter(self, label_set):
        '''Bla bla

        '''
        if label_set is None:
            collector = self.summaries
        else:
            collector = self._get_summary_subset(label_set)

        return iter(collector)

    def visualize_individual(self, entry_functions, label_set=None):
        '''Bla bla

        '''
        for summary in self._get_label_iter(label_set): 
            for retrieval_method in entry_functions:
                entry = getattr(summary, retrieval_method)()
                viz = Visualizer(write_output_format='html')
                for viz_method, viz_kwargs in self.viz_rundata[entry.key]:
                    namespace = self._randomword(15)
                    now = datetime.datetime.now().ctime()
                    getattr(viz, viz_method)(entry.value, **viz_kwargs)
                    viz.write_output(self.path_viz_out, namespace)
                    self._insert_db(summary.label, entry.key, viz_method, 
                                    self.path_viz_out, namespace, now)

    def visualize_union(self, union_func, entry_functions, label_set=None):
        '''Bla bla

        '''
        print (self.summaries)
        print (dir(self.summaries[0]))
        raise TypeError
        for summary in self._get_label_iter(label_set):
            for retrieval_method in entry_functions:
                entry = getattr(summary, retrieval_method)()

            

    def close_db(self):
        '''Bla bla
        
        '''
        self.db_conn.close()

    def __init__(self, iterof_summaries, path_out=None):
        '''Bla bla

        '''
        self.summaries = iterof_summaries
        self.path_viz_out = path_out

        self.db_conn = self._setup_db(path_out + '/viz.db')
        self.viz_rundata = HowToViz()
        self.viz_rundata.add_howto('backbone torsions', 'scatter_plot',
                        {'x_axis' : 'phi', 'y_axis' : 'psi', 
                         'level_name': 'property', 
                         'y_range' : (-180.0, 180.0), 
                         'x_range' : (-180.0, 180.0), 'alpha' : 0.5})
        self.viz_rundata.add_howto('number of residues', 'stacked_bars',
                        {'x_axis' : 'chain', 'y_axis' : 'residue count', 
                         'stack': 'property'}) 
        self.viz_rundata.add_howto('number of polarity residues', 'stacked_bars',
                        {'x_axis' : 'chain', 'y_axis' : 'residue count', 
                         'stack': 'property'}) 

