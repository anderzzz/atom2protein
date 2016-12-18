'''Bla bla

'''
from summaries import StructureSummary

class StructureAnalyzer:
    '''Bla bla

    '''
    def cmp_hydrogen_bonds(self, dist_cutoff=3.0, angle_cutoff=60.0):
        '''Bla bla

        '''
        pass

    def cmp_nresidue_polarity(self, structure):
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

        self.summary_object.add('number of residues', ret) 

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

        self.summary_object.add('number of polarity residues', ret) 

    def get_summary(self):
        '''Bla bla

        '''
        return self.summary_object

    def __init__(self):
        '''Bla bla

        '''
        self.summary_object = StructureSummary()

class Analyzer:
    '''Bla bla

    '''
    def __init__(self):
        '''Bla bla

        '''
        pass
