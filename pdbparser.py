'''Bla bla

'''
import xml.etree.ElementTree as etree
from protein_structure import Atom, ProteinResidue, Residue, Chain, Structure

class UnknownPDBType(Exception):
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
        '''Populate a protein structure object from an XML string.

        Args:
            xml_string (string): String of XML data in PDB format.

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

    def _populate_from_pdb(self, pdb_string):
        '''Populate a protein structure object from an PDB string. Currently
        not implemented.

        '''
        raise NotImplementedError('PDB parser based on text PDB file ' + \
                                  'not implemented. Consider the XML ' + \
                                  'version instead.') 

    def __init__(self, xml_string=None, pdb_string=None, xml_file=None):
        '''Initialize the protein structure parser.

        Args:
            xml_string (string): XML string of the structure in the PDML format.
            pdb_string (string): String of the structure in the PDB format.
            xml_file (string): Path to XML file to parse for structure in the
                               PDML format.

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

