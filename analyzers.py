'''Bla bla

'''
class StructureAnalyzer:
    '''Bla bla

    '''
    def cmp_hydrogen_bonds(self, structure):
        '''Bla bla

        '''
        pass

    def cmp_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        ret = {}
        for chain_label, chain in structure.items():
            n_res_pol = ret.setdefault(chain_label, {})
            for residue_label, residue in chain.items():
                if residue.is_protein_residue():
                    polarity = residue.polarity_class
                    n = n_res_pol.setdefault(polarity, 0)
                    n += 1
                    n_res_pol[polarity] = n
            ret[chain_label] = n_res_pol

        return ret 

    def cmp_nresidues(self, structure):
        '''Bla bla

        '''
        ret = {}
        for chain_label, chain in structure.items():
            n_res = ret.setdefault(chain_label, 0)
            for residue_label, residue in chain.items():
                if residue.is_protein_residue():
                    n_res += 1
            ret[chain_label] = n_res

        return ret 

    def __init__(self, hbond_dcutoff=3.0, hbond_acutoff=60.0):
        '''Bla bla

        '''
        self.hbond_dcutoff = hbond_dcutoff
        self.hbond_acutoff = hbond_acutoff

class Analyzer:
    '''Bla bla

    '''
    def __init__(self):
        '''Bla bla

        '''
        pass
