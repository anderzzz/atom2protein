'''Bla bla

'''
from bokeh.charts import Bar 
import pandas as pd
class Visualizer:
    '''Bla bla

    '''
    def __call__(self, summa):
        '''Bla bla

        '''
        tt = pd.DataFrame(summa.nresidues_polarity.value)
        print (tt)
        bar = Bar(tt, stack='property', label='chain', values='residue count')
        show(bar)
        raise TypeError

    def __init__(self):
        '''Bla bla

        '''
        pass
