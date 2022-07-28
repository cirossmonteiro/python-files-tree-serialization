import os
import shutil
import unittest

import commons

def create_random_ascii_file_in_folder(path):
    for n in range(5):
        with open(f'{path}/test_{n}.txt', 'w') as fh:
            fh.write(f'asdfg{n}')

class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.root = 'test_root/'
        os.mkdir('test_root')
        create_random_ascii_file_in_folder('test_root')
        os.mkdir('test_root/parent1')
        create_random_ascii_file_in_folder('test_root/parent1')
        os.mkdir('test_root/parent1/child1')
        create_random_ascii_file_in_folder('test_root/parent1/child1')
        os.mkdir('test_root/parent2')
        create_random_ascii_file_in_folder('test_root/parent2')
        os.mkdir('test_root/parent2/child2')
        create_random_ascii_file_in_folder('test_root/parent2/child2')
    
    def tearDown(self):
        shutil.rmtree('test_root')

    def test_serialization(self):
        root = commons.track_commons('.', self.root)
        self.assertIsInstance(root, commons.Commons)
        self.assertEqual(root.name, self.root)

        serialized = commons.serialize(root)
        unserialized = commons.unserialize(serialized)
        self.assertEqual(unserialized, root)

if __name__ == '__main__':
    unittest.main()