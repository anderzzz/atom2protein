import sys
import time

from webapis import PDBData
from webapis import PubMedData
from pubmed_entity import PubMedEntry

def main(args):

    pdb_data = PDBData(save_to_disk=True)
#    pdb_data.set_search_title('antibody')
#    pdb_data.set_search_title('HIV')
#    pdb_data.set_search_resolution(0.3, 1.0)
#    pdb_data.search()
#    pdb_data.set_id(['1A2y','1alz'])
#    for structure in pdb_data:
#        time.sleep(1)
#        print (structure)

    pmc_data = PubMedData(save_to_disk=True)
#    pmc_data.set_search_journal('science')
#    pmc_data.set_search_abstract('colon cancer')
#    pmc_data.set_search_publishdate('10060101','20161201')
#    pmc_data.search()
#    print (pmc_data.get_id())
#    for x in pmc_data:
#        time.sleep(2)
#        pubmed_entry = PubMedEntry(x)
#        print (x)
    f = open('pubmed_23118011.json')
    jj = f.read()
    print (jj)
    uu = PubMedEntry(jj)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
