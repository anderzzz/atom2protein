import sys
import time
import json
import numpy as np
import pprint

from rootdata import PDBData, PubMedData
from parsers import Parser
from summaries import StructureSummarizer
from presenter import Presenter, HowToViz

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

        presenter = Presenter(summarizer, path_viz_out, 
                              data_type_subset=['bb_torsions','nresidues_polarity'])
        presenter.produce_visualization()

        collector.append(summarizer)

    ht = HowToViz(default='summary structure')
    ht.add('bfactor_chain_stat', 'box_plot',
           {'values' : 'property statistics', 'label' : 'id'})
    presenter = Presenter(collector, path_viz_out, howtoviz=ht,
                          data_type_subset=['rresidues_polarity',
                                            'bb_torsions',
                                            'bfactor_chain_stat'])
    presenter.produce_visualization()



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
