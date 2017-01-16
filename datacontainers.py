'''Bla bla

'''
import itertools

class PMIDResetError(Exception):
    pass

class LevelError(Exception):
    pass

class StructureContainer:
    '''Class to define common methods and attributes for any structure
    container, that is anything but the atomic structure object. The class
    emulates a dictionary in how child elements are retrieved, while it
    emulates a set in how child emlements are added. The reason for this
    separation is that the key is not arbitrary, but contained in the child
    object label.

    '''
    def add(self, child_add):
        '''Method to add structure child object to the structure container. Can
        be another structure container object or an atomic structure object. If
        an object with the same label is found in the container, it is replaced
        with the new child object.

        Args:
            child_add (object): structure child object to add.

        Returns: None

        '''
        for index, child_object in enumerate(self.child_objects):
            if child_object.label == child_add.label:
                self.child_objects[index] = child_add
                break
        else:
            self.child_objects.append(child_add)

    def keys(self):
        '''Method to obtain the unique keys to access the child objects.

        Args: None

        Returns:
            keys (set): Set of strings of all keys to child structure objects.

        '''
        return set([child_object.label for child_object in self.child_objects])

    def items(self):
        '''Method to obtain iterator over (key, child_object).

        Args: None

        Returns: key_value (iterator): Iterator for tuple of string key and
                                       associated structure child object.

        '''
        for child_object in self.child_objects:
            yield (child_object.label, child_object)

    def unravel(self, level):
        '''Method to unravel a hierarchy of a structure container at a set
        level. Level equal to one is the same has the method items().

        Args:
            level (int): The number of levels to unravel of the container.

        Returns:
            objects (list): List of tuples, where the first element of tuple is
                            the combined structure label, where the second
                            element of tuple is the unravelled structure
                            object.

        '''
        def recurse(current, keys, dep):
            dep_new = dep - 1
            new_key = keys
            if dep_new == 0:
                coll.append((tuple(keys), current))
                return True
            for lab, val in current.items():
                recurse(val, new_key + [lab], dep_new)

        coll = []
        for lab, val in self.items():
            recurse(val, [lab], level)

        return coll

    def __getitem__(self, key):
        '''Method to obtain structure child object by string key.

        Args:
            key (string): String key to structure child object.

        Returns:
            child_object (object): Child object associated with given key.

        Raises:
            TypeError: If a non-string key given.
            KeyError: If the key is not found.

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
        '''Method to obtain iterator over keys.

        Args: None

        Returns:
            labels (iterator): Iterator over the string keys to each structure
                               child object.

        '''
        for child_object in self.child_objects:
            yield child_object.label

    def __init__(self, label):
        '''Method to initialize the general structure container object.

        Args:
            label (string): Label of the object. Must be unique within any set
                            of objects added to a parent structure object.

        '''
        self.label = label.lower()
        self.child_objects = []

class Structure(StructureContainer):
    '''Full protein structure container object. Children are typically one or
    more Chain structure objects.

    '''
    def set_experiment(self, experiment):
        '''Bla bla

        '''
        self.experimental_data = experiment

    def __init__(self, label='dummy', experimental_data=None):
        '''Method to initialize the full protein structure object.

        Args:
            label (string): Name of full protein structure.
            experimental_data (object, optional): Experiment object to characterize 
                                        how the structure was obtained.

        '''
        super().__init__(label)
        self.experimental_data = experimental_data

class Chain(StructureContainer):
    '''Chain structure container object. Children are typically
    one or more Residue or ProteinResidue objects.

    '''
    def get_backbone(self):
        '''Method to return a list of backbone atoms in the chain.

        Args: None.

        Returns:
            backbone (list):

        '''
        container = []
        for residue_label, residue in self.items():
            if residue.is_protein_residue():
                container.append((residue_label, residue.get_backbone_atoms()))

        return container

    def __init__(self, label, bio_content=None):
        '''Method to initialize the chain structure object.

        Args:
            label (string): Name of chain.
            bio_content (object, optional): TBD.

        '''
        super().__init__(label)
        self.bio_content = bio_content

class Residue(StructureContainer):
    '''Residue structure container object. Children are typically one or more
    atomic structure objects.

    '''
    def is_protein_residue(self):
        return False

    def get_backbone_atoms(self):
        return []

    def get_sidechain_atoms(self):
        return []

    def __str__(self):
        '''How to present residue object as string

        Args: None

        Returns:
            string_repr (string): String representation of residue.

        '''
        return 'Residue type %s of ID %s' %(self.residue_name_3lc, self.label)

    def __init__(self, name, residue_id, residue_insert='', description=None):
        '''Method to initialize the residue structure object.

        Args:
            name (string): Three letter code for the type of residue.
            residue_id (string): The residue id.
            residue_insert (string, optional): The residue insertion code in addition to
                                     the residue id.
            description (string, optional): A string description of the
                                  residue.

        '''
        super().__init__(residue_id + residue_insert)
        self.description = description
        self.residue_name_3lc = name.lower()

class ProteinResidue(Residue):
    '''Protein residue structure container object. Inherits the general Residue
    class. Children are typically one or more atomic structure objects.

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

    def code_convert(self, s):
        '''Method to convert between one and three letter protein residue
        codes.

        Args:
            s (string): The source code, either one or three letter.

        Returns:
            code (string): The code for the identical object as the input code,
                           only of the other kind of letter count.

        Raises:
            TypeError: In case code input is not a string of either one or
                       three characters.
            KeyError: In case a non-existant residue code is given.

        '''
        if len(s) == 3 and isinstance(s, str):
            n_type = 0
        elif len(s) == 1 and isinstance(s, str):
            n_type = 1
        else:
            raise TypeError('Protein residue code error. Must be string ' + \
                            'of either one or three characters')
            
        code_pair_index = [sc[n_type + 1 % 2] for sc in self.CODES if sc[n_type] == s]

        if len(code_pair_index) != 1:
            raise KeyError('Unsupported protein residue code: %s' %(s))

        return code_pair_index[0]

    def is_protein_residue(self):
        '''Check if residue is a protein residue.

        Args: None.

        Returns:
            yes_no (bool):

        '''
        return True

    def get_backbone_atoms(self):
        '''Return the backbone atoms of the residue.

        Args: None

        Returns:
            bb_atoms (list): List of backbone atom objects of residue.

        '''
        container = []
        for atom_label, atom in self.items():
            if atom_label in ['c', 'o', 'n', 'ca']:
                container.append(atom)

        return container

    def get_sidechain_atoms(self):
        '''Return the sidechain atoms of the residue.

        Args: None

        Returns:
            sc_atoms (list): List of sidechain atom objects of residue.

        '''
        bb_atom_labels = [x.label for x in self.get_backbone_atoms()]

        container = []
        for atom_label, atom in self.items():
            if atom_label in bb_atom_label:
                container.append(atom)

        return container

    def get_polarity(self, name):
        '''Retrieve the polarity class for a given protein residue type.

        Args:
            name (string): three letter code of residue type

        Returns:
            polarity (string): label for polarity class.

        '''
        return self._retrieve_property(name, 'polarity')

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

    def _retrieve_property(self, residue_key, property_name):
        '''General method to retrieve protein residue type properties from
        dictionary of class constants.

        Args:
            residue_key (string): three letter code of protein residue type.
            property_name (string): name of property to retrieve.

        Returns:
            property: constant property of residue type.

        Raises:
            KeyError: if either the residue or the property requested is absent
                      from the class constants.

        '''
        residue_key = residue_key.lower()
        if residue_key in self.RESIDUE_DATA:
            try:
                ret = self.RESIDUE_DATA[residue_key][property_name]
            except KeyError:
                raise KeyError('Undefined property %s' %(property_name))
        else:
            raise KeyError('Undefined residue %s' %(residue_key))

        return ret

    def __init__(self, name_3lc, residue_id, residue_insert='', secondary_structure=None):
        '''Method to initialize protein residue structure object. Normally a
        container for atomic structure objects.

        Args:
            name_3lc (string): Three letter code for the protein residue type.
            residue_id (string): Residue id within the chain.
            residue_insert (string, optional): Residue insertion code.
            secondary_structure (string, optional): Secondary structure the
                                                    protein residue part of.

        '''
        super().__init__(name_3lc, residue_id + residue_insert)
        self.residue_name_1lc = self.code_convert(name_3lc)
        self.polarity_class = self.get_polarity(self.residue_name_3lc)
        self.secondary_structure = self._validate_ss(secondary_structure)

class Atom:
    '''Class for the atomic structure object. This is an atom in a physical
    sense.

    '''
    ELEMENT_DATA = {'h' : {'mass' : 1.0},
                    'c' : {'mass' : 12.01},
                    'n' : {'mass' : 14.01},
                    'o' : {'mass' : 16.00},
                    's' : {'mass' : 32.07},
                    'p' : {'mass' : 30.97}}

    def _retrieve_property(self, element_key, property_name):
        '''General method to retrieve element properties from dictionary of 
        class constants.

        Args:
            element_key (string): element key. 
            property_name (string): name of property to retrieve.

        Returns:
            property: constant property of element.

        Raises:
            KeyError: if either the element or the property requested is absent
                      from the class constants.

        '''
        if element_key in self.ELEMENT_DATA:
            try:
                ret = self.ELEMENT_DATA[element_key][property_name]
            except KeyError:
                raise KeyError('Requested property missing: %s' %(property_name))
        else:
            raise KeyError('Undefined element %s' %(element_key))

        return ret

    def __init__(self, name, x, y, z, element, occupancy=None, bfactor=None, number=None):
        '''Initialize the atomic structure class.

        Args:
            name (string): unique atom name within the set of atoms in residue
            x: x-coordinate of atom.
            y: y-coordinate of atom.
            z: z-coordinate of atom.
            element (string): element key.
            occupancy (optional) : occupancy of atom in experimental method.
            bfactor (optional): B-factor of atom in experimental method.
            number (optional): numerical index of atom in experimental data.

        '''
        self.label = name
        self.coordinates = (float(x), float(y), float(z))
        self.occupancy = float(occupancy)
        self.bfactor = float(bfactor)
        self.element = element
        self.atom_index = int(number)
        self.atom_mass = self._retrieve_property(element, 'mass')

class PubMedContainer:
    '''Bla bla

    '''
    def set_journal_title(self, title):
        '''Bla bla

        '''
        self.journal_title = title

    def set_journal_title_abbreviation(self, title_abb):
        '''Bla bla

        '''
        self.journal_title_abb = title_abb

    def set_journal_year(self, year):
        '''Bla bla

        '''
        self.journal_year = int(year)

    def set_journal_volume(self, volume):
        '''Bla bla

        '''
        self.journal_volume = volume

    def set_journal_pages(self, pagination):
        '''Bla bla

        '''
        self.journal_pagination = pagination

    def set_article_title(self, title):
        '''Bla bla

        '''
        self.article_title = title

    def set_article_abstract(self, abstract_text):
        '''Bla bla

        '''
        self.article_abstract = abstract_text

    def set_pmid(self, pmid):
        '''Bla bla

        '''
        if self.pmid == None:
            self.pmid = int(pmid)
        else:
            raise PMIDResetError('PubMed ID already set. Changing it not an allowed operation')

    def get_pmid(self):
        '''Bla bla

        '''
        return self.pmid

    def __str__(self):
        '''Bla bla

        '''
        title_line = 'Article with title: "%s"' %(self.article_title)
        pubmed_id_line = 'Pubmed ID: %s' %(str(self.pmid))

        return title_line + '\n' + pubmed_id_line

    def __eq__(self, other):
        '''Bla bla

        '''
        pmid_1 = self.get_pmid()
        pmid_2 = other.get_pmid()

        return pmid_1 == pmid_2

    def __hash__(self):
        '''Bla bla

        '''
        return self.get_pmid()

    def __init__(self, pmid=None):
        '''Bla bla

        '''
        self.pmid = pmid
        self.article_title = None 
        self.article_abstract = None
        self.journal_title = None
        self.journal_title_abb = None
        self.journal_volume = None
        self.journal_year = None
        self.journal_pages = None

class PubMedCorpus:
    '''Bla bla

    '''
    def __iter__(self):
        '''Bla bla

        '''
        for entry in self.container:
            yield entry

    def __len__(self):
        '''Bla bla

        '''
        return len(self.container)

    def __init__(self):
        '''Bla bla

        '''
        self.container = set([]) 
