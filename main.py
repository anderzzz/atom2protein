import sys
import time

from webapis import PDBData
from webapis import PMCData

def main(args):

    pdb_data = PDBData(save_to_disk=True)
    pdb_data.set_pdbid(['1A2y','1alz'])
    for structure in pdb_data:
        time.sleep(1)
        print (structure)

    pmc_data = PMCData()
    pmc_data.set_search_term('colon+cancer+AND+science[journal]')
    pmc_data.search_pubmed()
    for x in pmc_data:
        time.sleep(2)
        print (x)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
