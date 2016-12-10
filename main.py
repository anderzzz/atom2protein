import sys

from webapis import PDBData

def main(args):

    print (args)
    pdb_data = PDBData()
    print (pdb_data.url_base)
    pdb_data.set_format_return('csv4')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
