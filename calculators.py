'''Bla bla

'''
import numpy as np
import pandas as pd

class StructureCalculator:
    '''Bla bla

    '''
    def _torsion_angle(self, atom_1, atom_2, atom_3, atom_4):
        '''Bla bla

        '''
        p0 = np.array(atom_1.coordinates)
        p1 = np.array(atom_2.coordinates)
        p2 = np.array(atom_3.coordinates)
        p3 = np.array(atom_4.coordinates)

        b0 = -1.0 * (p1 - p0)
        b1 = p2 - p1
        b2 = p3 - p2
        b1 = b1 / np.linalg.norm(b1)
        v = b0 - np.dot(b0, b1) * b1
        w = b2 - np.dot(b2, b1) * b1
        x = np.dot(v, w)
        y = np.dot(np.cross(b1, v), w)
        angle = np.degrees(np.arctan2(y, x))

        return angle

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

    def cmp_bb_torsions(self, structure):
        '''Bla bla

        '''
        ret = {}
        for label, chain in structure.unravel(level=1):
            bb_atoms = chain.get_backbone()
            for step in range(1, len(bb_atoms) - 1):
                ca_0 = bb_atoms[step - 1][1][1]
                c_0 = bb_atoms[step - 1][1][2]
                n_1 = bb_atoms[step][1][0]
                ca_1 = bb_atoms[step][1][1]
                c_1 = bb_atoms[step][1][2]
                n_2 = bb_atoms[step + 1][1][0]
                omega = self._torsion_angle(ca_0, c_0, n_1, ca_1)
                key = (label[0], int(bb_atoms[step][0]), 'omega')
                ret[key] = omega
                phi = self._torsion_angle(c_0, n_1, ca_1, c_1)
                key = (label[0], int(bb_atoms[step][0]), 'phi')
                ret[key] = phi
                psi = self._torsion_angle(n_1, ca_1, c_1, n_2)
                key = (label[0], int(bb_atoms[step][0]), 'psi')
                ret[key] = psi

        inds = pd.MultiIndex.from_tuples(ret.keys(),
                                         names=['chain','residue','property'])
        df = pd.Series(ret, index=inds, name='residue values')
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
