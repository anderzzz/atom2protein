'''Bla bla

'''
from webapis import PDBData
from parsers import Parser

class StatementCreator:
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        for data_class, data_methods in zip(self.class_container, self.methods):
            data_parser = Parser(data_class)

            for method in data_methods:
                func = getattr(data_class, method)
                func(**data_methods[method])
            data_class.search()

            for data in data_class:
                data_object = data_parser(data) 

        
    def __init__(self):
        '''Bla bla

        '''
        self.class_container = [PDBData()]
        self.methods = [{'set_search_title' : {'val':'antibody'},
                         'set_search_title' : {'val':'HIV'},
                         'set_search_resolution' : {'res_min':0.3,
                         'res_max':1.5}}]
