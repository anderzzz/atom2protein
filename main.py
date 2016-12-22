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

def main(args):

    data_parser = Parser(PDBData(), 'xml_file')
    path = '/home/anderzzz/ideas/protein/'
    pdb_files = ['protein_3tv3.xml', 'protein_3r0m.xml']
    collector = []
    for pdb_file in pdb_files:
        structure = data_parser(path + pdb_file)
        print (structure.label)

        summarizer = StructureSummarizer()
        summarizer.set_nresidues(structure)
        summarizer.set_nresidues_polarity(structure)
        summarizer.set_bfactor_chain_stat(structure)

        vis = Visualizer(pdb_file + '.html')
        vis.stacked_bars(summarizer.get_nresidues_polarity().unpack_value(),
                         x_axis='chain', y_axis='residue count',
                         stack='property', title='dummy')
        vis.make_html('/mnt/c/Users/Anders/Desktop/tmp2.html')
        raise TypeError
        collector.append(summarizer)

    ensemble_stat = EnsembleStat()
    ensemble_stat(collector)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
