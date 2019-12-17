import unittest
from siam_meta import SiamObj
from siam_meta import SiamSubj


class TestSiamMeta(unittest.TestCase):
    def setUp(self):
        self.siam_1 = SiamObj('1', '2', a=1, b=2)
        self.siam_2 = SiamObj('1', '2', b=2, a=1)
        self.siam_3 = SiamObj('11', '22', a=11, b=22)
        self.impostor_siam = SiamSubj('1', '2', a=1, b=2)

    def test_intra_class_equality(self):  #Verifies same-class objects equality
        self.assertEqual(self.siam_1, self.siam_2)

    def test_intra_class_inequality(self):  #Verifies same-class objects inequality
        self.assertNotEqual(self.siam_1, self.siam_3)

    def test_inter_class_inequality(self):  #Verifies inequality of similar objects of different classes
        self.assertNotEqual(self.siam_1, self.impostor_siam)
        self.assertNotEqual(self.siam_1.pool, self.impostor_siam.pool)

    def test_siam_bond(self):  #Verifies connection between class objects
        self.assertEqual(self.siam_3.connect('1', '2', 1, 2).a, 1)
        self.assertEqual(self.siam_3.connect('1', '2', b=2, a=1).a, 1)
        self.siam_3.connect('1', '2', 1, 2).a = 100
        self.assertEqual(self.siam_3.connect('1', '2', 1, 2).a, 100)

    def test_siam_annihilation(self):  #Verifies complete removal of deleted class objects
        pool = self.siam_3.pool
        self.assertEqual(len(pool), 2)
        del self.siam_3
        self.assertEqual(len(pool), 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=3)
