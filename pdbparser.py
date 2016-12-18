'''Bla bla

'''
import xml.etree.ElementTree as etree
from protein_structure import Atom, ProteinResidue, Residue, Chain, Structure
from functools import partial

class UnknownPDBType(Exception):
    pass

class UnknownFormatError(Exception):
    pass

class PDBParser:
    '''Class for parsing PDB structure file

    '''
    SUPPORTED_PDB_NS = ['{http://pdbml.pdb.org/schema/pdbx-v40.xsd}']

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
        if not namespace in self.SUPPORTED_PDB_NS:
            raise UnknownPDBType('Unknown namespace encountered: %s' %(namespace))

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
                    residue_new = ProteinResidue(residue_name, residue_index)
                elif residue_type == 'hetatm':
                    residue_new = Residue(residue_name, residue_index)
                else:
                    raise KeyError('Unsupported residue type %s' %(residue_type))
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

        return structure

    def _populate_from_pdb(self, pdb_string):
        '''Populate a protein structure object from an PDB string. Currently
        not implemented.

        '''
        raise NotImplementedError('PDB parser based on text PDB file ' + \
                                  'not implemented. Consider the XML ' + \
                                  'version instead.') 

    def _populate_from_xml_file(self, xml_path):
        '''Bla bla

        '''
        with open(xml_path) as fin:
            xml_string = fin.read()
        return self._populate_from_xml(xml_string)

    def _populate_from_pdb_file(self, pdb_path):
        '''Bla bla

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
