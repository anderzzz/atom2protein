'''Bla bla

'''
from webapis import PDBData
from parsers import Parser

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

            primitive_parser = Parser(root_obj)
            for data in root_obj:
                primitive = primitive_parser(data) 
                summarizer = Summarizer(primitive, **self.summarize_init[k_run])
                for summary_method in self.summarize_stream:
                    func = getattr(summarizer, summary_method)
                    func(primitive)
                print (summarizer)


        
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
        self.summarize_stream.append(['set_nresidue', 'set_nresidue_polarity'])
