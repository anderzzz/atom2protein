'''Bla bla

'''
from summaries import Entry

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

    def __init__(self):
        '''Bla bla

        '''
        pass
