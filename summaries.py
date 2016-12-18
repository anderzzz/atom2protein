'''Bla bla

How to make this nice and general for the statistics module? Lets go full blown
object oriented... in some way.
'''
import json
from collections import namedtuple

Entry = namedtuple('Entry', ['key','value','description'])

class StructureSummary:
    '''Bla bla

    '''
    def add(self, key, value, description=None):
        '''Bla bla

        '''
        if key == 'number of residues':
            self.nres_per_chain = Entry(key, value, description)
        elif key == 'number of polarity residues':
            self.nres_per_chain_polarity = Entry(key, value, description)
        else:
            raise KeyError('Unknown summary type')

    def make_json(self):
        '''Bla bla

        '''
        pass

    def __init__(self):
        '''Bla bla

        '''
        self.nres_per_chain = None 
        self.nres_per_chain_polarity = None 
