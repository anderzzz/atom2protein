'''Bla bla

'''
class PDBParser:
    '''Bla bla

    '''
    PDBLINE = {'HEADER' : 'header',
               'TITLE ' : 'structure title',
               'COMPND' : 'compound definitions',
               'SOURCE' : 'source of protein',
               'KEYWDS' : 'keywords',
               'EXPDTA' : 'structure determination method',
               'AUTHOR' : 'authors',
               'SEQRES' : 'sequence',
               'HETNAM' : 'non-protein residues',
               'HELIX ' : 'helix range',
               'SHEET ' : 'sheet range',
               'SSBOND' : 'disulphide bonds',
               'ATOM  ' : 'protein structure data',
               'TER   ' : 'chain termination',
               'HETATM' : 'non-protein structure data',
               'CONECT' : 'atom connection',
               'MASTER' : 'master line',
               'END   ' : 'file termination'}

    PDBREMARK = {'REMARK    2' : 'xray resolution',
                 'REMARK    3' : 'refinement metadata'}

    def _type_of_line(self, text):
        '''Bla bla

        '''
        col1 = text[0:6]
        if col1 in PDB2NEW:
            ret_val = PDBLINE[col1]
        else:
            if col1 == 'REMARK':
                col12 = text[0:10]
                ret_val = PDBREMARK[col2]
            else:
                ret_val = None

        return ret_val

    def _populate_from_pdb(self, pdb_string):
        '''Bla bla

        '''
        lines = pdb_string.split('\n')
        for line in lines:
            type_of_line = self._type_of_line(line) 

    def __init__(self, pdb_string=None):
        '''Bla bla

        '''
        if not pdb_string is None:
            self._populate_from_pdb(pdb_string)

class Experiment:
    '''Bla bla

    '''
    def __init__(self, method, resolution=None, ph=None, temp=None):
        '''Bla bla

        '''
        self.method = method
        self.resolution = resolution
        self.ph = ph
        self.temp = temp

class Structure:
    '''Bla bla

    '''
    def append(self, chain_object):
        '''Bla bla

        '''
        self.chains.append(chain_object)

    def __iter__(self):
        '''Bla bla

        '''
        for chain in self.chains:
            yield chain

    def __init__(self, title=None, pdb_id=None, experimental_data=None):
        '''Bla bla

        '''
        self.title = title
        self.pdb_id = pdb_id
        self.experimental_data = experimental_data
        self.chains = []

class Chain:
    '''Bla bla

    '''
    def append(self, residue_object):
        '''Bla bla

        '''
        self.residues.append(residue_object)

    def __iter__(self):
        '''Bla bla

        '''
        for res in self.residues:
            yield res

    def __init__(self, label, bio_content=None):
        '''Bla bla

        '''
        self.label = label
        self.residues = []
        self.bio_content = bio_content

class Residue:
    '''Bla bla

    '''
    def append(self, atom_object):
        '''Bla bla

        '''
        self.atoms.append(atom_object)

    def __iter__(self):
        '''Bla bla

        '''
        for atom in self.atoms:
            yield atom

    def __init__(self, name_3lc, residue_id, description=None):
        '''Bla bla

        '''
        self.name_3lc = name_3lc
        self.index = int(residue_id)
        self.description = description
        self.atoms = []

class ProteinResidue(Residue):
    '''Bla bla

    '''
    CODES = [('ala', 'a'), ('cys', 'c'), ('glu', 'e'), ('gln', 'q'), 
             ('gly', 'g'), ('asp', 'd'), ('asn', 'n'), ('arg', 'r'),
             ('lys', 'k'), ('pro', 'p'), ('leu', 'l'), ('ile', 'i'),
             ('val', 'v'), ('thr', 't'), ('ser', 's'), ('tyr', 'y'),
             ('phe', 'f'), ('trp', 'w'), ('met', 'm'), ('his', 'h')]

    RESIDUE_DATA = {'ala' : {'polarity' : 'hydrophobic'},
                    'asp' : {'polarity' : 'negative charge'}}

    SS_DATA = {'helix' : {}, 'sheet' : {}, 'loop' : {}}

    def _code_conversion(self, s, n_type):
        '''Bla bla

        '''
        code_pair_index = [sc[n_type + 1 % 2] for sc in self.CODES if s[n_type] == s]
        if len(code_pair_index) != 1:
            raise KeyError('Unsupported protein residue code: %s' %(s))

        return code_pair_index[0]

    def _validate_ss(self, ss_string):
        '''Bla bla

        '''
        if ss_string is None:
            ret = None
        else:
            if ss_string.lower() in self.SS_DATA:
                ret = ss_string.lower()
            else:
                raise KeyError('Unknown secondary structure type: %s' %(ss_string))

        return ret

    def code3_to_1(self, s):
        '''Bla bla

        '''
        return self._code_conversion(s.lower(), 0)

    def code1_to_3(self, s):
        '''Bla bla

        '''
        return self._code_conversion(s.lower(), 1)

    def retrieve_property(self, residue_key, property_name):
        '''Bla bla

        '''
        if residue_key in RESIDUE_DATA:
            ret = RESIDUE_DATA[residue_key][property_name]
        else:
            raise KeyError('Undefined residue %s' %(s))

        return ret

    def __init__(self, name_3lc, secondary_structure=None):
        '''Bla bla

        '''
        super.__init__(name_3lc)
        self.residue_name_1lc = self.code3_to_1(name_3lc)
        self.residue_polarity_class = self.set_polarity(name_3lc)
        self.secondary_structure = self._validate_ss(secondary_structure)

class Atom:
    '''Bla bla

    '''
    ELEMENT_DATA = {'H' : {'mass' : 1.0},
                    'C' : {'mass' : 12.01},
                    'N' : {'mass' : 14.01},
                    'O' : {'mass' : 16.00},
                    'S' : {'mass' : 32.07},
                    'P' : {'mass' : 30.97}}

    def retrieve_property(self, element_key, property_name):
        '''Bla bla

        '''
        if element_key in ELEMENT_DATA:
            ret = ELEMENT_DATA[element_key][property_name]
        else:
            raise KeyError('Undefined element %s' %(element_key))

        return ret

    def __init__(self, name, x, y, z, occupancy, bfactor, element, number):
        '''Bla bla

        '''
        self.atom_name = name
        self.coordinates = (float(x), float(y), float(z))
        self.occupancy = float(occupancy)
        self.bfactor = float(bfactor)
        self.element = element
        self.atom_index = int(number)
        self.atom_mass = self.retrieve_property(element, 'mass')

