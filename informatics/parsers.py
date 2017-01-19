'''Bla bla

'''
import xml.etree.ElementTree as etree

from informatics.rawretrievers import PDBData, PubMedData
from informatics.datacontainers import Atom, ProteinResidue, Residue, Chain, Structure
from informatics.datacontainers import NonNaturalResidueError

class UnknownDataType(Exception):
    pass

class UnknownPDBType(Exception):
    pass

class UnknownFormatError(Exception):
    pass

class XMLPathError(Exception):
    pass

class PDBParser:
    '''Class for parsing PDB structure file

    '''
    def _get_pdb_namespace(self, xml_root):
        '''Method to retrieve the XML namespace from the root.

        Args:
            xml_root (object): The XML root from the ElementTree class.

        Returns:
            namespace (string): XML namespace.

        '''
        if xml_root.tag[-9:] != 'datablock':
            namespace = None
        else:
            namespace = xml_root.tag[0:-9]

        return namespace

    def _find_text(self, tag, collection, namespace):
        '''Find text in the XML atom record.

        Args:
            tag (string): The tag to retrieve text from.
            collection (object): The atom XML collection object to parse.
            namespace (string): The namespace of the XML object.

        Returns:
            text (string): The text found in the atom XML collection for given
                           tag. If tag not found, returns None.

        '''
        text = collection.find('./%s%s' %(namespace, tag)).text
        if text is None:
            ret = None 
        else:
            ret = text.lower()

        return ret

    def _populate_from_xml(self, xml_string):
        '''Populate structure object with metadata from an XML string.

        Args:
            xml_string (string): String of XML data in PDBML format.

        '''
        structure = self._populate_structure_from_xml(xml_string)
        experiment = self._populate_experiment_from_xml(xml_string)
        structure.set_experiment(experiment)

        return structure

    def _populate_experiment_from_xml(self, xml_string):
        '''Bla bla

        '''
        pass

    def _populate_structure_from_xml(self, xml_string):
        '''Populate a protein structure object from an XML string.

        Args:
            xml_string (string): String of XML data in PDBML format.

        '''
        residue_index_prev = -1
        residue = None
        chain_name_prev = '-1'
        chain = None

        root = etree.fromstring(xml_string) 
        pdb_code = root.attrib['datablockName']
        namespace = self._get_pdb_namespace(root)
        if namespace is None:
            raise UnknownPDBType('Could not locate namespace in PDB')

        structure = Structure(label=pdb_code)
        atoms = root.findall('.//%satom_site' %(namespace))
        # Loop over all atoms in structure and populate structure object
        for atom in atoms:
            atom_index = atom.attrib['id']
            x_coord = self._find_text('Cartn_x', atom, namespace)
            y_coord = self._find_text('Cartn_y', atom, namespace)
            z_coord = self._find_text('Cartn_z', atom, namespace)
            b_factor = self._find_text('B_iso_or_equiv', atom, namespace)
            element = self._find_text('type_symbol', atom, namespace)
            occ = self._find_text('occupancy', atom, namespace)
            name = self._find_text('auth_atom_id', atom, namespace)
            residue_name = self._find_text('auth_comp_id', atom, namespace)
            residue_index = self._find_text('auth_seq_id', atom, namespace)
            residue_type = self._find_text('group_PDB', atom, namespace)
            chain_name = self._find_text('auth_asym_id', atom, namespace)
            residue_atom = Atom(name, x_coord, y_coord, z_coord,
                                element, occupancy=occ, bfactor=b_factor,
                                number=atom_index)

            # If a new residue is encountered, create new residue object
            if residue_index != residue_index_prev:
                if residue_type == 'atom':
                    # This try-except clause needed because of bug in how
                    # external XML file handles non-natural residues. Bug
                    # report filed to RCSB on 2017-01-19.
                    try:
                        residue_new = ProteinResidue(residue_name, residue_index)
                    except NonNaturalResidueError:
                        residue_new = Residue(residue_name, residue_index)
                elif residue_type == 'hetatm':
                        residue_new = Residue(residue_name, residue_index)
                else:
                    raise RuntimeError('Unknown atom type %s encountered' %(residue_type))
                residue_index_prev = residue_index

                # Add the old residue object to the current chain object
                if residue != None:
                    chain.add(residue)

                # Reset the current residue to the new residue
                residue = residue_new

                # If a new chain is encountered, create new chain object, or
                # retrieve the incomplete chain object already in structure
                if chain_name != chain_name_prev:

                    # Add the old chain to the structure
                    if chain != None:
                        structure.add(chain)

                    # If the chain already exist in the structure, retrieve it
                    # and continue to add to it
                    if chain_name in structure.keys():
                        chain = structure[chain_name]
                    else:
                        chain = Chain(chain_name)
                    chain_name_prev = chain_name

            # Add atom to current residue
            residue.add(residue_atom)
        structure.add(chain)

        return structure

    def _populate_from_pdb(self, pdb_string):
        '''Populate a protein structure object from an PDB string. Currently
        not implemented.

        '''
        raise NotImplementedError('PDB parser based on text PDB file ' + \
                                  'not implemented. Consider the XML ' + \
                                  'version instead.') 

    def _populate_from_xml_file(self, xml_path):
        '''Populate structure object with metadata from an XML file.

        Args:
            xml_path (string): Path to XML file with PDBML data.

        '''
        with open(xml_path) as fin:
            xml_string = fin.read()

        return self._populate_from_xml(xml_string)

    def _populate_from_pdb_file(self, pdb_path):
        '''Populate a protein structure object from an PDB string. Currently
        not implemented.

        '''
        with open(pdb_path) as fin:
            pdb_string = fin.read()

        return self._populate_from_pdb(pdb_string)

    def __call__(self, data):
        '''Call the initialized parser to process the data

        Args:
            data: the data to parse in a format as initialized

        Returns: None

        '''
        return self.populator_method(data)

    def __init__(self, data_format_signifier='xml_string'):
        '''Initialize the protein structure parser.

        Args:
            data_format_signifier (string): A string that defines the format of
                                            the structure data to be parsed.
                                            Valid options are: 'xml_string',
                                            'pdb_string', 'xml_file',
                                            'pdb_file', where 'xml_string' is
                                            default.

        Returns: PDBParser object.

        Raises: 
            UnknownFormatError: if specified format of data to parse is
                                unknown.

        '''
        if data_format_signifier == 'xml_string':
            self.populator_method = self._populate_from_xml
        elif data_format_signifier == 'pdb_string':
            self.populator_method = self._populate_from_pdb
        elif data_format_signifier == 'xml_file':
            self.populator_method = self._populate_from_xml_file
        elif data_format_signifier == 'pdb_file':
            self.populator_method = self._populate_from_pdb_file
        else:
            raise UnknownFormatError('Unknown data format: %s' %(data_format_signifier))

class PubMedParser:
    '''Class to parse output from a PubMed Web API search.

    '''
    def _get_and_check(self, root, path, default=''):
        '''Check if text is found at a specified tag in the PubMed XML string.

        Args:
            root (object): The XML root object from ElementTree
            path (string): The path to the desired tag
            default (string, optional): The default return value in case no
                                        text is found.

        Returns:
            text (string): The text found at specified path.

        Raises:
            XMLPathError: If tag is present, but text undefined.

        '''
        element = root.find(path)
        if element is None:
            ret = default
        else:
            ret = element.text
            if len(ret.strip()) == 0:
                raise XMLPathError('The path %s returned empty text')

        return ret

    def _populate_from_xml(self, xml_string):
        '''Populates the PubMed object based on the data retrieved from the
        PubMed XML string.

        Args:
            xml_string (string): The XML string to parse

        Returns:
            entry (object): The PubMedEntry object with attributes populated in
                            accordance with data in XML.

        '''
        root = etree.fromstring(xml_string)

        medline_root = './PubmedArticle/MedlineCitation/'
        article_root = medline_root + 'Article/'

        entry = PubMedEntry()
        entry.set_pmid(self._get_and_check(root, 
                       medline_root + 'PMID'))
        entry.set_journal_title(self._get_and_check(root, 
                                article_root + 'Journal/Title')) 
        entry.set_journal_title_abbreviation(self._get_and_check(root,
                                             article_root + 'Journal/ISOAbbreviation')) 
        entry.set_journal_volume(self._get_and_check(root,
                                 article_root + 'Journal/JournalIssue/Volume'))
        entry.set_journal_year(self._get_and_check(root,
                               article_root + 'Journal/JournalIssue/PubDate/Year'))
        entry.set_article_title(self._get_and_check(root,
                                article_root + 'ArticleTitle'))
        entry.set_article_abstract(self._get_and_check(root,
                                   article_root + 'Abstract/AbstractText'))
        entry.set_journal_pages(self._get_and_check(root,
                                article_root + 'Pagination/MedlinePgn'))

        return entry

    def __call__(self, data):
        '''Parse PubMed data and return a PubMedEntry object.

        Args:
            data: XML string or path to XML file with the PubMed data as
                  obtained from a web search.

        Returns:
            entry (object): The PubMedEntry object with attributes populated in
                            accordance with data in XML.

        '''
        return self.populator_method(data)

    def __init__(self, data_format_signifier='xml_string'):
        '''Initialize a PubMed data parser.

        Args:
            data_format_signifier (string): The format the data will be
                                            received in. Valid values are
                                            'xml_string' if data is XML string,
                                            'xml_file' if data is in XML file.

        Returns: PubMedParser object.

        Raises:
            UnknownFormatError: If format of data is unknown.

        '''
        if data_format_signifier == 'xml_string':
            self.populator_method = self._populate_from_xml
        elif data_format_signifier == 'xml_file':
            self.populator_method = self._populate_from_xml_file
        else:
            raise UnknownFormatError('Unknown data format: %s' %(data_format_signifier))

class Parser:
    '''Class to parse protein raw data and populate instance of relevant data
    container.
    
    Class for a general data type parser, where the specific parser is
    selected on basis of the data type. This is a factory class to
    enable general use. A class instance returns a data container when called
    with raw data as input argument..

    Parameters
    ----------
    data_type, raw data object
        The raw data object to be parsed. Can be any type.
    args, tuple, optional
        A tuple of arguments to pass to specific raw data parser.

    Returns
    -------
    data_container, object
        The data container object associated with the raw data type. The
        specific content of the data container is populated from the raw data
        passed as an argument to the class instance.

    Notes
    -----
    The associations between raw data class and data container currently
    implemented are:

    +------------------+-----------------------+-------------------+
    | Raw Data Class   | Data Container Class  | Parser Class      |
    +==================+=======================+===================+
    | PDBData          | StructureContainer    | PDBParser         |
    +------------------+-----------------------+-------------------+
    | PubMedData       | PubMedContainer       | PubMedParser      |
    +------------------+-----------------------+-------------------+

    Raises
    ------
    UnknownDataType
        If class of input object is not associated with any specific parser.

    '''
    def __call__(self, data):
        '''Parse specific raw data and return data container.

        Parameters
        ----------
        data, raw data object
            Raw data to be parsed in any valid format.

        Returns
        -------
        object, data container object 
            Data container object with attributes populated from the parsed 
            raw data.

        '''
        return self.parser(data)
        
    def __init__(self, data_type, *args):

        if isinstance(data_type, PDBData):
            self.parser = PDBParser(*args)
        elif isinstance(data_type, PubMedData):
            self.parser = PubMedParser(*args) 
        else:
            raise UnknownDataType('No parser exist for data type %s' %(type(data_type)))
