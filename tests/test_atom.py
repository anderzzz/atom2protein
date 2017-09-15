'''Bla bla

'''
import unittest

from informatics.datacontainers import Atom

class TestAtomSetup(unittest.TestCase):

    def setUp(self):
        self.atom = Atom('test atom', 2.0, 3.0, 4.0, 'C')

    def test_atom_mass(self):
        self.assertEqual(self.atom.atom_mass, 12.01)

if __name__ == '__main__':
    unittest.main()
