'''Bla bla

'''
from rawretrievers import PDBData
from parsers import Parser
from summaries import Summarizer
from ensemble_stat import EnsembleStat

from collections import namedtuple

class StatementCreator:
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        for k_run, root_obj in enumerate(self.root):
            for search_method in self.search_stream:
                func = getattr(root_obj, search_method)
                func(**self.search_stream[search_method])
            root_obj.search()

            summary_collection = []
            primitive_parser = Parser(root_obj)
            for data in root_obj:
                primitive = primitive_parser(data) 
                summarizer = Summarizer(primitive, **self.summarize_init[k_run])
                summarizer.set_label(primitive.label)
                for summary_method in self.summarize_stream:
                    func = getattr(summarizer, summary_method)
                    func(primitive)
                summary_collection.append(summarizer)

            ensemble_stat = EnsembleStat(make_graphics=True, **self.stat_init[k_run])
            ensemble_stat(summary_collection)
        
    def __init__(self):
        '''Bla bla

        '''
        self.root = [] 
        self.search_stream = []
        self.summarize_init = []
        self.summarize_stream = []

        self.root.append(PDBData())
        self.search_stream.append({'set_search_title' : {'val':'antibody'},
                                   'set_search_title' : {'val':'HIV'},
                                   'set_search_resolution' : {'res_min':0.3,
                                   'res_max':1.5}})
        self.summarize_init.append({})
        self.summarize_stream.append(['set_nresidue', 'set_rresidue_polarity'])
