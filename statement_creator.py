'''Bla bla

'''
from webapis import PDBData
from parsers import Parser

from collections import namedtuple

ActionSet = namedtuple('ActionSet', ['root', 'methods'])

class StatementCreator:
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        for search, analyze in zip(self.search_stream, self.analyze_stream):
            primitive_parser = Parser(search.root)

            for method in search.methods:
                func = getattr(search.root, method)
                func(**search.root[method])
            search.root.search()

            for data in search.root:
                primitive = primitive_parser(data) 
                for method in analyze.methods:
                    func = getattr(analyze.root, method)
                    func(**analyze.root[method])
                summary = analyze.root.get_summary()


        
    def __init__(self):
        '''Bla bla

        '''
        self.search_stream = []
        self.analyze_stream = []

        action = ActionSet(PDBData(), {'set_search_title' : {'val':'antibody'},
                                       'set_search_title' : {'val':'HIV'},
                                       'set_search_resolution' : {'res_min':0.3,
                                       'res_max':1.5}})
        self.search_stream.append(action)
        action = ActionSet(StructureAnalyzer(), {'cmp_nresidue' : {},
                                                 'cmp_nresidue_polarity' : {}})
        self.analyze_stream.append(action)
