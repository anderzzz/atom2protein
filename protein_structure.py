'''Bla bla

'''
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

class StructureContainerObject:
    '''Bla bla

    '''
    def add(self, child_add):
        '''Bla bla

        '''
        for index, child_object in enumerate(self.child_objects):
            if child_object.label == child_add.label:
                self.child_objects[index] = child_add
                break
        else:
            self.child_objects.append(child_add)

    def keys(self):
        '''Bla bla

        '''
        return set([child_object.label for child_object in self.child_objects])

    def items(self):
        '''Bla bla

        '''
        for child_object in self.child_objects:
            yield (child_object.label, child_object)

    def __getitem__(self, key):
        '''Bla bla

        '''
        if not isinstance(key, str):
            raise TypeError('Key to structure object must be string')
        for child_object in self.child_objects:
            if child_object.label == key:
                break
        else:
            raise KeyError('Structure object with key %s not found' %(key))

        return child_object

    def __iter__(self):
        '''Bla bla

        '''
        for child_object in self.child_objects:
            yield child_object.label

    def __init__(self, label):
        '''Bla bla

        '''
        self.label = label.lower()
        self.child_objects = []

class Structure(StructureContainerObject):
    '''Bla bla

    '''
    def __init__(self, label='dummy', experimental_data=None):
        '''Bla bla

        '''
        super().__init__(label)
        self.experimental_data = experimental_data

class Chain(StructureContainerObject):
    '''Bla bla

    '''
    def __init__(self, label, bio_content=None):
        '''Bla bla

        '''
        super().__init__(label)
        self.bio_content = bio_content

class Residue(StructureContainerObject):
    '''Bla bla

    '''
    def __init__(self, name, residue_id, residue_insert='', description=None):
        '''Bla bla

        '''
        super().__init__(residue_id + residue_insert)
        self.description = description
        self.residue_name_3lc = name.lower()

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

    def __init__(self, name_3lc, residue_id, residue_insert='', secondary_structure=None):
        '''Bla bla

        '''
        super().__init__(name_3lc, residue_id + residue_insert)
        self.residue_name_1lc = self.code3_to_1(name_3lc)
        self.residue_polarity_class = self.get_polarity(self.residue_name_3lc)
        self.secondary_structure = self._validate_ss(secondary_structure)

class Atom:
    '''Bla bla

    '''
    ELEMENT_DATA = {'h' : {'mass' : 1.0},
                    'c' : {'mass' : 12.01},
                    'n' : {'mass' : 14.01},
                    'o' : {'mass' : 16.00},
                    's' : {'mass' : 32.07},
                    'p' : {'mass' : 30.97}}

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
        self.label = name
        self.coordinates = (float(x), float(y), float(z))
        self.occupancy = float(occupancy)
        self.bfactor = float(bfactor)
        self.element = element
        self.atom_index = int(number)
        self.atom_mass = self._retrieve_property(element, 'mass')

