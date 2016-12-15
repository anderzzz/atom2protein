import sys
import time

from webapis import PDBData
from webapis import PubMedData
from pubmed_entity import PubMedCorpus
from protein_structure import PDBParser

def main(args):

#    pdb_data = PDBData(save_to_disk=True)
#    pdb_data.set_search_title('antibody')
#    pdb_data.set_search_title('HIV')
#    pdb_data.set_search_resolution(0.3, 1.5)
#    pdb_data.search()
#    pdb_data.set_id(['1A2y','1alz'])
#    for structure in pdb_data:
#        time.sleep(1)
#        print (structure)

#    pmc_data = PubMedData(save_to_disk=True)
#    pmc_data.set_search_journal('science')
#    pmc_data.set_search_abstract('colon cancer')
#    pmc_data.set_search_publishdate('20060101','20161201')
#    pmc_data.search()
#    pubmed_corpus = PubMedCorpus()
#    for x in pmc_data:
#        pubmed_corpus.append(x)

 #   print (pubmed_corpus.container)
 #   print (len(pubmed_corpus))
#    f = open('pubmed_23118011.json')
#    jj = f.read()
#    print (jj)
#    uu = PubMedEntry(jj)

    f = open('protein_3r0m.xml')
    xml_string = f.read()
    parser = PDBParser(xml_string=xml_string)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
