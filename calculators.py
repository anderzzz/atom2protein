'''Bla bla

'''
import numpy as np
import pandas as pd

class StructureCalculator:
    '''Bla bla

    '''
    def _statify(self, array):
        '''Bla bla

        '''
        ret = {}
        for stat_label, stat_func in self.stat_cmp.items():
            val = stat_func(array)
            if not (isinstance(val, float) or isinstance(val, int)):
                raise InvalidFunctionType('Statitics function labelled %s ' + \
                      'does not return float or int.' %(stat_label))
            ret[stat_label] = val

        return ret

    def cmp_hydrogen_bonds(self, structure):
        '''Bla bla

        '''
        pass

    def cmp_bfactor_chain_stat(self, structure):
        '''Bla bla

        '''
        ret = {}
        for label, chain in structure.unravel(level=1):
            data_array = []
            for residue_label, residue in chain.items():
                if residue.is_protein_residue():
                    for atom_label, atom in residue.items():
                        data_array.append(atom.bfactor)

            stat_props = self._statify(data_array) 
            for stat_prop in stat_props:
                key = tuple([x for x in label] + [stat_prop])
                ret[key] = stat_props[stat_prop]

        inds = pd.MultiIndex.from_tuples(ret.keys(), names=['chain', 'B-factor property'])
        df = pd.Series(ret, index=inds, name='property statistics')
        df.sort_index(inplace=True)

        return df 
                        
    def cmp_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        ret = {} 
        for label, chain in structure.unravel(level=1):
            for residue_label, residue in chain.items():
                if residue.is_protein_residue():
                    polarity = residue.polarity_class
                    key = tuple([x for x in label] + [polarity])
                    count = ret.setdefault(key, 0)
                    count += 1
                    ret[key] = count

        inds = pd.MultiIndex.from_tuples(ret.keys(), names=['chain', 'property'])
        df = pd.Series(ret, index=inds, name='residue count')
        df.sort_index(inplace=True)

        return df 

    def cmp_nresidues(self, structure):
        '''Bla bla

        '''
        ret = {}
        for label, chain in structure.unravel(level=1):
            for residue_label, residue in chain.items():
                if residue.is_protein_residue():
                    key = tuple([x for x in label] + ['total count']) 
                    count = ret.setdefault(key, 0)
                    count += 1
                    ret[key] = count

        inds = pd.MultiIndex.from_tuples(ret.keys(), names=['chain', 'property'])
        df = pd.Series(ret, index=inds, name='residue count')
        df.sort_index(inplace=True)

        return df 

    def __init__(self, hbond_dcutoff=3.0, hbond_acutoff=60.0, 
                 stat_cmp={'minimum' : np.amin, 'maximum' : np.amax, 
                           'median' : np.median, 'mean' : np.mean, 'std' : np.std}):
        '''Bla bla

        '''
        self.hbond_dcutoff = hbond_dcutoff
        self.hbond_acutoff = hbond_acutoff
        self.stat_cmp = stat_cmp 

class Calculator:
    '''Bla bla

    '''
    def __init__(self):
        '''Bla bla

        '''
        pass
