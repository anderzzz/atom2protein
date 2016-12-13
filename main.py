import sys
import time

from webapis import PDBData
from webapis import PMCData

def main(args):

    pdb_data = PDBData(save_to_disk=True)
    pdb_data.set_search_title('antibody')
    pdb_data.set_search_title('HIV')
#    pdb_data.set_search_resolution(0.3, 1.0)
    pdb_data.search()
#    pdb_data.set_id(['1A2y','1alz'])
    for structure in pdb_data:
        time.sleep(1)
        print (structure)

    pmc_data = PMCData(save_to_disk=True)
    pmc_data.set_search_term('colon+cancer+AND+science[journal]')
    pmc_data.search()
    for x in pmc_data:
        time.sleep(2)
        print (x)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
