'''Module that defines all internal data objects, typically populated by a
parser applied to raw data.

'''
class PMIDResetError(Exception):
    pass

class NonNaturalResidueError(Exception):
    pass

class StructureContainer:
    '''Class to define common methods and attributes for any structure
    container, that is anything but the atomic structure object. 
    
    The class emulates a dictionary in how child elements are retrieved, 
    while it emulates a set in how child emlements are added. The reason 
    for this separation is that the key is not arbitrary, but contained 
    in the child object label.

    Parameters
    ----------
    label : string 
        Label of the object. Must be unique within any set of objects 
        added to a parent structure object.

    Notes
    -----
    Child objects of a structure class instance can be accessed via the string 
    key of the child object.

    Like a dictionary the child objects can be iterated over. 

    '''
    def add(self, child_add):
        '''Method to add structure child object to the structure container. 
        
        The child object that is added can
        be another structure container object or an atomic structure object. If
        an object with the same label is found in the container, it is replaced
        with the new child object.

        Parameters
        ----------
        child_add : object 
            Structure child object to add.

        '''
        for index, child_object in enumerate(self.child_objects):
            if child_object.label == child_add.label:
                self.child_objects[index] = child_add
                break
        else:
            self.child_objects.append(child_add)

    def keys(self):
        '''Method to obtain the unique keys to access the child objects.

        Returns
        -------
        keys : set
            Set of strings of all keys to child structure objects.

        '''
        return set([child_object.label for child_object in self.child_objects])

    def items(self):
        '''Obtain iterator over (key, child_object).

        Yields
        ------
        key_value : tuple 
            Tuple of string key and associated structure child object.

        '''
        for child_object in self.child_objects:
            yield (child_object.label, child_object)

    def unravel(self, level):
        '''Unravel a hierarchy of a structure container at a set
        level. 
        
        The recursive unraveling of the structure object into key value 
        pairs where the higher the level, the further down the hierarchy the
        unraveling goes. Level equal to one is the same has the method
        ``items``.

        Parameters
        ----------
        level : int
            The number of levels to unravel of the container.

        Returns
        -------
        objects : list 
            List of tuples, where the first element of tuple is
            the combined structure element label, where the second
            element of tuple is the unravelled structure object.

        Notes
        -----
        The keys for the unravelled key-value pair are tuples of an increasing
        length with increasing value of ``level``. Each element is a label of a
        structure child object.

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

        Parameters
        ----------
        key : string
            String key to structure child object.

        Returns
        -------
        child_object : object
            Child object associated with given key.

        Raises
        ------
        TypeError 
            If a non-string key given.
        KeyError
            If the key is not found.

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

        Yields
        ------
        labels : object
            The string keys to each structure child object.

        '''
        for child_object in self.child_objects:
            yield child_object.label

    def __init__(self, label):
        self.label = label.lower()
        self.child_objects = []

class Structure(StructureContainer):
    '''Full protein structure container object. 
    
    Inherits from the StructureContainer class, where child objects typically
    are instances of Chain class.

    Parameters
    ----------
    label : string, default "no label"
        Arbitrary but unique label of structure, preferably PDB ID.
    experimental_data : object, optional
        Experiment object to characterize how structure data was experimentally
        obtained.

    '''
    def set_experiment(self, experiment):
        '''Set the experiment attribute of the structure.

        Parameters
        ----------
        experiment : object
            The Experiment object with data on how structure was experimentally
            obtained.

        '''
        self.experimental_data = experiment

    def __init__(self, label='no label', experimental_data=None):
        super().__init__(label)
        self.experimental_data = experimental_data

class Chain(StructureContainer):
    '''Chain structure container object. 
    
    Children are typically one or more Residue or ProteinResidue objects. These
    are populated typically by a parser applied to raw data.

    Parameters
    ----------
    label : string
        String label for chain object, must be unique within its super
        structure container.
    bio_content : object, optional
        Object to define the biological content of the chain (not implemented).

    '''
    def get_backbone(self):
        '''Method to return a list of backbone atoms in the chain.

        Returns
        -------
        backbone : list
            List of Atom objects that correspond to backbone atoms in the
            chain.

        '''
        container = []
        for residue_label, residue in self.items():
            if residue.is_protein_residue():
                container.append((residue_label, residue.get_backbone_atoms()))

        return container

    def __init__(self, label, bio_content=None):
        super().__init__(label)
        self.bio_content = bio_content

class Residue(StructureContainer):
    '''Residue structure container object. 
    
    Children are typically one or more atomic structure objects. This is the
    general residue class, which is expanded and modified by the
    ``ProteinResidue`` class.

    Parameters
    ----------
    name : string 
        Three letter code for the type of residue.
    residue_id : string
        The residue id, which together with ``residue_insert`` forms a unique
        identifier for within the Chain.
    residue_insert : string, optional
        The residue insertion code in addition to the residue id.
    description, string, optional
        A string description of the residue.

    '''
    def is_protein_residue(self):
        return False

    def get_backbone_atoms(self):
        return []

    def get_sidechain_atoms(self):
        return []

    def __str__(self):
        '''How to present residue object as string.

        Returns
        -------
        string_repr : string
            String representation of residue.

        '''
        return 'Residue type %s of ID %s' %(self.residue_name_3lc, self.label)

    def __init__(self, name, residue_id, residue_insert='', description=None):
        super().__init__(residue_id + residue_insert)
        self.description = description
        self.residue_name_3lc = name.lower()

class ProteinResidue(Residue):
    '''Protein residue structure container object. 
    
    Inherits the general Residue class. Children are typically one or more 
    atomic structure objects. The class contains protein residue constants.

    Parameters
    ----------
    name_3lc : string
        Three letter code for the protein residue type.
    residue_id : string
        Residue id within the chain.
    residue_insert : string, optional
        Residue insertion code.
    secondary_structure : string, optional
        Secondary structure the protein residue part of.

    Raises
    ------
    NonNaturalResidueError
        In case a non-natural residue type, based on the name, is given.

    '''
    CODES = [('ala', 'a'), ('cys', 'c'), ('glu', 'e'), ('gln', 'q'), 
             ('gly', 'g'), ('asp', 'd'), ('asn', 'n'), ('arg', 'r'),
             ('lys', 'k'), ('pro', 'p'), ('leu', 'l'), ('ile', 'i'),
             ('val', 'v'), ('thr', 't'), ('ser', 's'), ('tyr', 'y'),
             ('phe', 'f'), ('trp', 'w'), ('met', 'm'), ('his', 'h')]
    '''list: List of tuples that associate one-letter and three-letter codes
    for protein residue.

    '''

    NATURAL_PRES = [name_3lc for name_3lc, name_1lc in CODES]
    '''list: List of three letter codes for natural protein residues.

    '''

    RESIDUE_DATA = {'ala' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'asp' : {'polarity' : 'negative charge',
                             'chemical' : 'carboxylic acid'},
                    'asn' : {'polarity' : 'hydrophilic',
                             'chemical' : 'amide'},
                    'arg' : {'polarity' : 'positive charge',
                             'chemical' : 'guanidine'},
                    'cys' : {'polarity' : 'hydrophobic',
                             'chemical' : 'thiol'},
                    'gly' : {'polarity' : 'hydrophilic',
                             'chemical' : 'aliphatic'},
                    'gln' : {'polarity' : 'hydrophilic',
                             'chemical' : 'amide'},
                    'glu' : {'polarity' : 'negative charge',
                             'chemical' : 'carboxylic acid'},
                    'lys' : {'polarity' : 'positive charge',
                             'chemical' : 'amine'},
                    'pro' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'leu' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'ile' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'val' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'thr' : {'polarity' : 'hydrophilic',
                             'chemical' : 'alcohol'},
                    'ser' : {'polarity' : 'hydrophilic',
                             'chemical' : 'alcohol'},
                    'tyr' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aromatic'},
                    'phe' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aromatic'},
                    'trp' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aromatic'},
                    'met' : {'polarity' : 'hydrophobic',
                             'chemical' : 'aliphatic'},
                    'his' : {'polarity' : 'hydrophilic',
                             'chemical' : 'imidazole'}}
    '''dict: Residue properties, keyed on three-letter code.

    Dictionary of dictionaries of protein residue properties. Properties
    includes:
    * ``polarity`` : classification of each residue in terms of polarity.
    * ``chemical`` : classification of each residue in terms of chemical
      structure of side-chain.

    '''

    SS_DATA = {'helix' : {}, 'sheet' : {}, 'loop' : {}}

    def code_convert(self, s):
        '''Method to convert between one and three letter protein residue
        codes.

        Parameters
        ----------
        s : string
            The source code, either one or three letter.

        Returns
        -------
        code : string
            The code for the identical object as the input code,
            only of the other kind of letter count.

        Raises
        ------
        TypeError
            In case code input is not a string of either one or 
            three characters.
        KeyError
            In case a non-existant residue code is given.

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

        Returns
        -------
        yes_no : bool
            True for protein residues

        '''
        return True

    def get_backbone_atoms(self):
        '''Return the backbone atoms of the residue.

        Returns
        -------
        bb_atoms : list
            List of backbone atom objects of residue.

        '''
        container = []
        for atom_label, atom in self.items():
            if atom_label in ['c', 'o', 'n', 'ca']:
                container.append(atom)

        return container

    def get_sidechain_atoms(self):
        '''Return the sidechain atoms of the residue.

        Returns
        -------
        sc_atoms : list
            List of sidechain atom objects of residue.

        '''
        bb_atom_labels = [x.label for x in self.get_backbone_atoms()]

        container = []
        for atom_label, atom in self.items():
            if atom_label in bb_atom_label:
                container.append(atom)

        return container

    def get_polarity(self):
        '''Retrieve the polarity class for residue.

        Returns
        -------
        polarity : string
            Label for residue polarity class.

        '''
        return self._retrieve_property(self.residue_name_3lc, 'polarity')

    def _validate_ss(self, ss_string):
        '''Validate that a given secondary structure string is defined as a
        constant.

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

        Parameters
        ----------
        residue_key : string
            Three letter code of protein residue type.
        property_name : string
            Name of property to retrieve.

        Returns
        -------
        property : string, int, or float 
            Constant property of residue type.

        Raises
        ------
        KeyError
            If either the residue or the property requested is absent from 
            the class constants.

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

        if not name_3lc.lower() in self.NATURAL_PRES:
            raise NonNaturalResidueError("Unsupported Non-Natural Residue provided.")

        super().__init__(name_3lc, residue_id + residue_insert)
        self.residue_name_1lc = self.code_convert(name_3lc)
        self.polarity_class = self.get_polarity()
        self.secondary_structure = self._validate_ss(secondary_structure)

class Atom:
    '''Class for the atomic structure object. This is an atom in a physical
    sense.

    Parameters
    ----------
    name : string
        Unique atom name within the set of atoms in residue
    x : float
        x-coordinate of atom.
    y : float
        y-coordinate of atom.
    z : float
        z-coordinate of atom.
    element : string
        Element key, as defined in the Periodic Table.
    occupancy : float, optional, default 1.0
        Occupancy of atom in experimental method.
    bfactor : float, optional
        B-factor of atom in experimental method.
    number : int, optional
        Numerical index of atom in experimental data.

    '''
    ELEMENT_DATA = {'h' : {'mass' : 1.0},
                    'c' : {'mass' : 12.01},
                    'n' : {'mass' : 14.01},
                    'o' : {'mass' : 16.00},
                    's' : {'mass' : 32.07},
                    'p' : {'mass' : 30.97},
                    'li' : {'mass' : 6.94},
                    'f' : {'mass' : 19.00},
                    'na' : {'mass' : 22.99},
                    'cl' : {'mass' : 35.45},
                    'k' : {'mass' : 39.10},
                    'ca' : {'mass' : 40.08},
                    'fe' : {'mass' : 55.85},
                    'cu' : {'mass' : 63.55},
                    'br' : {'mass' : 79.90}}
    '''dict: Properties of relevant elements.

    The properties include:
    * ``mass`` : atomic mass of element.

    '''
    def _retrieve_property(self, element_key, property_name):
        '''General method to retrieve element properties from dictionary of 
        class constants.

        Parameters
        ----------
        element_key : string
            Element key as defined in the Periodic Table. 
        property_name : string
            Name of property to retrieve.

        Returns
        -------
        property : string, int, float
            Constant property of element.

        Raises
        ------
        KeyError
            If either the element or the property requested is absent
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

    def __init__(self, name, x, y, z, element, occupancy=1.0, bfactor=None, number=None):
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

