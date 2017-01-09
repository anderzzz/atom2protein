'''Bla bla

'''
from visualizer import Visualizer
from summarizer import StructureSummarizer, PubMedSummarizer

import collections

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

    def _ensemble_wrapper(self, func):
        '''Bla bla

        '''
        def make_ensemble(self):
                
            if self.ensemble_summary:
                self.summary_object = self.ensemble_maker(self.summary_object)
            else:
                pass

            return func

        return make_ensemble

    def _produce_visualization(self):
        '''Bla bla

        '''

    def close_db(self):
        '''Bla bla
        
        '''
        self.db_conn.close()

    def make_ensemble(self, **kwargs):
        '''Bla bla

        '''
        if self.ensemble_maker is None:
            self.ensemble_maker = Ensemble


    def __init__(self, summary_object, howtoviz=None, ensemble_method='join',
                 db_path='vizfiles.db'):
        '''Bla bla

        '''
        self.summary_object = summary_object
        self.howtoviz = None

        if isinstance(self.summary_object, collections.Iterable):
            self.ensemble_summary = True
            if self.howtoviz is None:
                if all(isinstance(s, StructureSummarizer) for s in
                       self.summary_object):
                    self.howtoviz = HowToViz(default='summary structure')
                elif all(isinstance(s, PubMedSummarizer) for s in
                       self.summary_object):
                    self.howtoviz = HowToViz(default='summary pubmed')
                else:
                    raise TypeError("Summary contains objects without a presenter class")
        else:
            self.ensemble_summary = False
            if self.howtoviz is None:
                if isinstance(self.summary_object, StructureSummarizer):
                    self.howtoviz = HowToViz(default='single structure')
                elif isinstance(self.summary_object, PubMedSummarizer):
                    self.howtoviz = HowToViz(default='single pubmed')
                else:
                    raise TypeError("Summary is of type without a presenter class")

        self.ensemble_maker = EnsembleMaker(ensemble_method)

        self.produce_visualization = self._make_ensemble(self._produce_visualization)

        self.db_conn = self._setup_db(out_file_path=db_path)
