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
    pdb_files = ['protein_3r0m.xml', 'protein_3tv3.xml']
    collector = []
    for pdb_file in pdb_files:
        structure = data_parser(path + pdb_file)
        print (structure.label)

        summarizer = StructureSummarizer()
        summarizer.set_nresidues(structure)
        summarizer.set_nresidues_polarity(structure)
        summarizer.set_bfactor_chain_stat(structure)

        vis = Visualizer()
        vis(summarizer)
        raise TypeError
        collector.append(summarizer)

    ensemble_stat = EnsembleStat()
    ensemble_stat(collector)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
