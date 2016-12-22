import sys
import time
import json
import numpy as np
import pprint

from rootdata import PDBData, PubMedData
from parsers import Parser
from summaries import StructureSummarizer
from ensemble_stat import EnsembleStat
from visualizers import Visualizer

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
    path = '/home/anderzzz/ideas/protein/'
    pdb_files = ['protein_3tv3.xml', 'protein_1wm3.xml']
    collector = []
    for pdb_file in pdb_files:
        structure = data_parser(path + pdb_file)
        print (structure.label)

        summarizer = StructureSummarizer()
        summarizer.set_nresidues(structure)
        summarizer.set_nresidues_polarity(structure)
        summarizer.set_bfactor_chain_stat(structure)
        summarizer.set_bb_torsions(structure)

        print (summarizer.unpack_nresidues_polarity())
        print (summarizer.unpack_bfactor_chain_stat())
        print (summarizer.unpack_bb_torsions())
        vis = Visualizer()
        vis.scatter_plot(summarizer.unpack_bb_torsions(), x_axis='phi',
                         y_axis='psi', x_range=(-180.0, 180.0),
                         y_range=(-180.0, 180.0))
        vis.stacked_bars(summarizer.get_nresidues_polarity().unpack_value(),
                         x_axis='chain', y_axis='residue count',
                         stack='property', title='dummy')
        vis.make_html('/mnt/c/Users/Anders/Desktop/tmp%s.html' %(structure.label))
        collector.append(summarizer)

    #ensemble_stat = EnsembleStat()
    #ensemble_stat(collector)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
