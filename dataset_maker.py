'''Bla bla

'''
from webapis import PDBData

class DataSetMaker:
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        for data_class, data_methods in zip(self.class_container, self.methods):
            for method in data_methods:
                func = getattr(data_class, method)
                func(**data_methods[method])

            data_class.search()

            print (type(data_class))
            raise TypeError
            for data in data_class:
                PDBParser(data)

        
    def __init__(self):
        '''Bla bla

        '''
        self.class_container = [PDBData()]
        self.methods = [{'set_search_title' : {'val':'antibody'},
                         'set_search_depositdate' : {'date_min':'20101201',
                         'date_max':'20111201'}}]
