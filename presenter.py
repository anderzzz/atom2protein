'''Bla bla

'''
from visualizers import Visualizer
from summaries import StructureSummarizer, PubMedSummarizer
from ensemble_makers import EnsembleMaker

import inspect
import sqlite3
import datetime
import random
import string

class HowToViz:
    '''Bla bla

    '''
    def add(self, data_entry, method_name, kwargs_dict):
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

    def __init__(self, default=None):
        '''Bla bla

        '''
        self.container = {}
        self.available_viz_methods = set([name for name, method in
                                     inspect.getmembers(Visualizer,
                                     predicate=inspect.isfunction)])

        if default == 'single structure':
            self.add('bb_torsions', 'scatter_plot', 
                     {'x_axis' : 'phi', 'y_axis' : 'psi',
                      'level_name' : 'property',
                      'y_range' : (-180.0, 180.0),
                      'x_range' : (-180.0, 180.0),
                      'alpha' : 0.5})
            self.add('nresidues', 'stacked_bars',
                     {'x_axis' : 'chain', 'y_axis' : 'residue count',
                      'stack' : 'property'})
            self.add('nresidues_polarity', 'stacked_bars',
                     {'x_axis' : 'chain', 'y_axis' : 'residue count',
                      'stack' : 'property'})

        elif default == 'summary structure':
            self.add('bb_torsions', 'scatter_plot',
                     {'x_axis' : 'phi', 'y_axis' : 'psi',
                      'level_name' : 'property',
                      'y_range' : (-180.0, 180.0),
                      'x_range' : (-180.0, 180.0),
                      'alpha' : 0.5})
            self.add('nresidues_polarity', 'spider_plot',
                     {'dims' : 'property', 'common_range' : (0.0, 1.0)})

        elif default == 'single pubmed':
            pass
        elif default == 'summary pubmed':
            pass
        elif default is None:
            pass
        else:
            raise KeyError("Undefined default given: %s" %(default))
        
class Presenter:
    '''Bla bla

    '''
    def _randomword(self, length):
        '''Bla bla

        '''
        return ''.join(random.choice(string.ascii_lowercase +
                                     string.digits) for i in range(length))

    def _setup_db(self, out_file_path):
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

    def produce_visualization(self):
        '''Bla bla

        '''
        for entry_type in self.type_subset:
            entry = self.summary_object[entry_type]
            viz = Visualizer(write_output_format='html')
            for viz_method, viz_kwargs in self.howtoviz[entry_type]:
                namespace = self._randomword(15)
                now = datetime.datetime.now().ctime()
                getattr(viz, viz_method)(entry.value, **viz_kwargs)
                viz.write_output(self.file_path, namespace)
                self._insert_db(self.summary_object.label, entry.brief,
                                viz_method, self.file_path, namespace, now)
        raise TypeError

    def _validate_subset(self, summary_obj, id_subset, type_subset):
        '''Bla bla
       
        '''
        ids = set([])
        types = set([])
        if isinstance(summary_obj, (list, set, tuple)):
            for s in summary_obj:
                ids.add(s.label)
                types = types.union(set(s._get_live_entries()))
        else:
            ids.add(summary_obj.label)
            types = types.union(set(summary_obj._get_live_entries()))

        if id_subset is None:
            ret_1 = ids
        else:
            ret_1 = set(id_subset)
        if type_subset is None:
            ret_2 = types
        else:
            ret_2 = set(type_subset)

        if not ret_1.issubset(ids):
            raise KeyError("Summary ID subset not subset of IDs of given summary")
        if not ret_2.issubset(types):
            raise KeyError("Summary data types subset not subset of data types of given summary")
            
        return ret_1, ret_2

    def close_db(self):
        '''Bla bla
        
        '''
        self.db_conn.close()

    def __init__(self, summary_object, file_path, 
                 howtoviz=None, ensemble_operation='join',
                 db_path='vizfiles.db', id_subset=None, data_type_subset=None):
        '''Bla bla

        '''
        self.file_path = file_path
        self.howtoviz = howtoviz 
        self.id_subset, self.type_subset = self._validate_subset(summary_object, 
                                                     id_subset, data_type_subset)

        if isinstance(summary_object, (list, set, tuple)):
            self.ensemble_summary = True
            self.ensemble_maker = EnsembleMaker(ensemble_operation,
                                                self.id_subset)
            if self.howtoviz is None:
                if all(isinstance(s, StructureSummarizer) for s in summary_object):
                    self.howtoviz = HowToViz(default='summary structure')
                elif all(isinstance(s, PubMedSummarizer) for s in summary_object):
                    self.howtoviz = HowToViz(default='summary pubmed')
                else:
                    raise TypeError("Summary contains objects without a presenter class")
        else:
            self.ensemble_summary = False
            self.ensemble_maker = EnsembleMaker('unity', None)
            if self.howtoviz is None:
                if isinstance(summary_object, StructureSummarizer):
                    self.howtoviz = HowToViz(default='single structure')
                elif isinstance(summary_object, PubMedSummarizer):
                    self.howtoviz = HowToViz(default='single pubmed')
                else:
                    raise TypeError("Summary is of type without a presenter class")

        self.summary_object = self.ensemble_maker(summary_object)

        self.db_conn = self._setup_db(out_file_path=db_path)

