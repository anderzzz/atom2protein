import sys
import time
import json
import numpy as np
import pprint

from rootdata import PDBData, PubMedData
from parsers import Parser
from summaries import StructureSummarizer
from ensemble_stat import EnsembleStat

def search_pdb():
    pdb_root = PDBData(save_to_disk=True)
    pdb_parser = Parser(pdb_root, 'xml_string')
    pdb_root.set_search_resolution(1.0, 1.2)
    pdb_root.set_search_title('sumo')
    pdb_root.search()
    for structure_root in pdb_root:
        structure_primitive = pdb_parser(structure_root)
        print (structure_primitive.label)
        summarizer = StructureSummarizer()
        summarizer.set_nresidues(structure_primitive)
        summarizer.set_nresidues_polarity(structure_primitive)
        summarizer.set_bfactor_chain_stat(structure_primitive)
        print (summarizer.unpack_nresidues())
        print (summarizer.unpack_nresidues_polarity())
        print (summarizer.unpack_bfactor_chain_stat())
#        vis = Visualizer()
#        vis.stacked_bars(summarizer.get_nresidues_polarity().unpack_value(),
#                         x_axis='chain', y_axis='residue_count', 
#                         stack='property', title=structure_primitive.label)
#        vis.make_html('/mnt/c/Users/Anders/Desktop/tmp2.html')
        print ('\n\n') 

def main(args):

#    search_pdb()
#    sys.exit() 

    data_parser = Parser(PDBData(), 'xml_file')
    path_viz_out = '/home/anderzzz/ideas/protein/viz_output'
    path = '/home/anderzzz/ideas/protein/'
    pdb_files = ['protein_3tv3.xml', 'protein_1wm3.xml',
    'protein_3a4r.xml','protein_3r0m.xml','protein_3d9a.xml']
    collector = []
    for pdb_file in pdb_files:
        structure = data_parser(path + pdb_file)
        print (structure.label)

        summarizer = StructureSummarizer(structure.label)
        summarizer.populate_nresidues(structure)
        summarizer.populate_nresidues_polarity(structure)
        summarizer.populate_rresidues_polarity(structure)
        summarizer.populate_bfactor_chain_stat(structure)
        summarizer.populate_bb_torsions(structure)

        collector.append(summarizer)

    ensemble_stat = EnsembleStat(collector, path_viz_out)
    ensemble_stat.visualize_individual(label_set=['3tv3','1wm3'],
                                       entry_types=['bb_torsions',
                                                    'nresidues',
                                                    'nresidues_polarity'])
    ensemble_stat.visualize_union('join',
                                  label_set=['3tv3','1wm3','3d9a'],
                                  entry_functions=['nresidues_polarity'])
    ensemble_stat.close_db()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
