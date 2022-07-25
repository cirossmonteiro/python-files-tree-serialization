import os
import unittest

import utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.bin'
        self.alphabet = list(range(65, 91)) # uppercase
        self.size = 10
        self.index = 10
        self.first_part = self.alphabet[:self.index]
        self.nulls = [0 for _ in range(self.size)]
        self.second_part = self.alphabet[self.index:]
        with open(self.filename, 'wb') as fh:
            fh.write(bytes(self.alphabet))
    
    def tearDown(self):
        os.remove(self.filename)

    def test_shift_right(self):
        utils.insert_null(self.filename, 10, 10)
        with open(self.filename, 'rb') as fh:
            self.assertEqual(fh.read(), bytes([*self.first_part, *self.nulls, *self.second_part]))

if __name__ == '__main__':
    unittest.main()
