'''Bla bla

'''
import xml.etree.ElementTree as etree

class UnknownPDBType(Exception):
    pass

class PDBParser:
    '''Bla bla

    '''
    # Set constants
    SUPPORTED_PDB_NS = ['{http://pdbml.pdb.org/schema/pdbx-v40.xsd}']

    def _get_pdb_namespace(self, xml_root):
        '''Bla bla

        '''
        if xml_root.tag[-9:] != 'datablock':
            namespace = None
        else:
            namespace = xml_root.tag[0:-9]

        return namespace

    def _populate_from_xml(self, xml_string):
        '''Bla bla

        '''
        residue_index_prev = -1
        residue = None
        chain_name_prev = '-1'
        chain = None
        structure = Structure()

        root = etree.fromstring(xml_string) 
        namespace = self._get_pdb_namespace(root)
        if namespace is None:
            raise UnknownPDBType('Could not locate namespace in PDB')
        if not namespace in self.SUPPORTED_PDB_NS:
            raise UnknownPDBType('Unknown namespace encountered: %s' %(namespace))

        atoms = root.findall('.//%satom_site' %(namespace))
        for atom in atoms:
            atom_index = atom.attrib['id']
            x_coord = atom.find('./%sCartn_x' %(namespace)).text
            y_coord = atom.find('./%sCartn_y' %(namespace)).text
            z_coord = atom.find('./%sCartn_z' %(namespace)).text
            b_factor = atom.find('./%sB_iso_or_equiv' %(namespace)).text
            element = atom.find('./%stype_symbol' %(namespace)).text
            occ = atom.find('./%soccupancy' %(namespace)).text
            name = atom.find('./%sauth_atom_id' %(namespace)).text
            
            residue_atom = Atom(name, x_coord, y_coord, z_coord,
                                occ, b_factor, element, atom_index)

            residue_name = atom.find('./%sauth_comp_id' %(namespace)).text
            residue_index = atom.find('./%sauth_seq_id' %(namespace)).text
            residue_type = atom.find('./%sgroup_PDB' %(namespace)).text

            if residue_index != residue_index_prev:
                if residue_type == 'ATOM':
                    residue_new = ProteinResidue(residue_name, residue_index)
                elif residue_type == 'HETATM':
                    residue_new = Residue(residue_name, residue_index)
                else:
                    raise KeyError('Unsupported residue type %s' %(residue_type))
                residue_index_prev = residue_index
                if residue != None:
                    chain.append(residue)

                chain_name = atom.find('./%sauth_asym_id' %(namespace)).text
                if chain_name != chain_name_prev:
                    if chain != None:
                        structure.add(chain)

                    print (structure.keys())
                    if chain_name in structure.keys():
                        chain = structure[chain_name]
                    else:
                        chain = Chain(chain_name)

                    chain_name_prev = chain_name
                residue = residue_new

            residue.append(residue_atom)

        print (structure)
        for c in structure:
            print (c.label)


    def _populate_from_pdb(self, pdb_string):
        '''Bla bla

        '''
        raise NotImplementedError('PDB parser based on text PDB file ' + \
                                  'not implemented. Consider the XML ' + \
                                  'version instead.') 

    def __init__(self, xml_string=None, pdb_string=None, xml_file=None):
        '''Bla bla

        '''
        # Populate structure from file or string parsing
        if not pdb_string is None:
            self._populate_from_pdb(pdb_string)
        if not xml_string is None:
            self._populate_from_xml(xml_string)
        if not xml_file is None:
            with open(xml_file) as fin:
                xml_data = fin.read()
                self._populate_from_xml(xml_data)

class Experiment:
    '''Bla bla

    '''
    def __init__(self, method=None, resolution=None, ph=None, temp=None,
                 authors=None):
        '''Bla bla

        '''
        self.method = method
        self.resolution = resolution
        self.ph = ph
        self.temp = temp
        self.authors = authors

class Structure:
    '''Bla bla

    '''
    def add(self, chain_object):
        '''Bla bla

        '''
        for index, chain in enumerate(self.chains):
            if chain.label == chain_object.label:
                self.chains[index] = chain_object
                break
        else:
            self.chains.append(chain_object)

    def keys(self):
        '''Bla bla

        '''
        return set([chain.get_label() for chain in self.chains])

    def __getitem__(self, key):
        '''Bla bla

        '''
        if not isinstance(key, str):
            raise TypeError('Key to structure elements should be string')
        for chain in self.chains:
            if chain.label == key:
                break
        else:
            raise KeyError('Chain key %s not found in structure')

        return chain

    def __setitem__(self, key, value):
        '''Bla bla

        '''
        if not isinstance(key, str):
            raise TypeError('Key to structure elements should be string')
        if not isinstance(value, Chain):
            raise TypeError('Structure elements should be Chain objects')
        self.chains.append(value)

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

    def get_label(self):
        '''Bla bla

        '''
        return self.label

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
        self.residue_name_3lc = name_3lc.lower()
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
                    'asp' : {'polarity' : 'negative charge'},
                    'asn' : {'polarity' : 'hydrophilic'},
                    'arg' : {'polarity' : 'positive charge'},
                    'cys' : {'polarity' : 'hydrophobic'},
                    'gly' : {'polarity' : 'hydrophilic'},
                    'gln' : {'polarity' : 'hydrophilic'},
                    'glu' : {'polarity' : 'negative charge'},
                    'lys' : {'polarity' : 'positive charge'},
                    'pro' : {'polarity' : 'hydrophobic'},
                    'leu' : {'polarity' : 'hydrophobic'},
                    'ile' : {'polarity' : 'hydrophobic'},
                    'val' : {'polarity' : 'hydrophobic'},
                    'thr' : {'polarity' : 'hydrophilic'},
                    'ser' : {'polarity' : 'hydrophilic'},
                    'tyr' : {'polarity' : 'hydrophobic'},
                    'phe' : {'polarity' : 'hydrophobic'},
                    'trp' : {'polarity' : 'hydrophobic'},
                    'met' : {'polarity' : 'hydrophobic'},
                    'his' : {'polarity' : 'hydrophilic'}}

    SS_DATA = {'helix' : {}, 'sheet' : {}, 'loop' : {}}

    def _code_conversion(self, s, n_type):
        '''Bla bla

        '''
        code_pair_index = [sc[n_type + 1 % 2] for sc in self.CODES if sc[n_type] == s]
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

    def get_polarity(self, name):
        '''Bla bla

        '''
        return self._retrieve_property(name, 'polarity')

    def _retrieve_property(self, residue_key, property_name):
        '''Bla bla

        '''
        if residue_key in self.RESIDUE_DATA:
            ret = self.RESIDUE_DATA[residue_key][property_name]
        else:
            raise KeyError('Undefined residue %s' %(residue_key))

        return ret

    def __init__(self, name_3lc, residue_id, secondary_structure=None):
        '''Bla bla

        '''
        super().__init__(name_3lc, residue_id)
        self.residue_name_1lc = self.code3_to_1(name_3lc)
        self.residue_polarity_class = self.get_polarity(self.residue_name_3lc)
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

    def _retrieve_property(self, element_key, property_name):
        '''Bla bla

        '''
        if element_key in self.ELEMENT_DATA:
            ret = self.ELEMENT_DATA[element_key][property_name]
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
        self.atom_mass = self._retrieve_property(element, 'mass')

