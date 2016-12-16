'''Bla bla

'''
import xml.etree.ElementTree as etree
from protein_structure import Atom, ProteinResidue, Residue, Chain, Structure

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

    def _find_text(self, tag, collection, namespace):
        '''Bla bla

        '''
        text = collection.find('./%s%s' %(namespace, tag)).text
        if text is None:
            ret = None 
        else:
            ret = text.lower()

        return ret

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

            if residue_index != residue_index_prev:
                if residue_type == 'atom':
                    residue_new = ProteinResidue(residue_name, residue_index)
                elif residue_type == 'hetatm':
                    residue_new = Residue(residue_name, residue_index)
                else:
                    raise KeyError('Unsupported residue type %s' %(residue_type))
                residue_index_prev = residue_index
                if residue != None:
                    chain.add(residue)

                if chain_name != chain_name_prev:
                    if chain != None:
                        structure.add(chain)

                    print (chain_name, structure.keys())
                    if chain_name in structure.keys():
                        chain = structure[chain_name]
                        print ('aaa')
                    else:
                        chain = Chain(chain_name)

                    chain_name_prev = chain_name
                residue = residue_new

            residue.add(residue_atom)

        for label, c in structure.items():
            for idr, r in c.items():
                for nn, a in r.items():
                    print (label, idr, nn, a)


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

