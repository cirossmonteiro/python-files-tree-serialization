import os
import unittest

import fs

class TestFS(unittest.TestCase):
    def setUp(self):
        self.name = 'test'
        self.filename = f'{self.name}.fs'

    def tearDown(self):
        os.remove(self.filename)

    def test_start_fs(self):
        fsystem = fs.FS(self.name)
        self.assertTrue(os.path.isfile(self.filename))
        self.assertEqual(fsystem.raw(True), [2, 46, 47, 0])
        self.assertEqual(fsystem.total_size(), 7) #1+2+4+0

        folder = fsystem.current_folder()
        self.assertIsInstance(folder, fs.Folder)

if __name__ == '__main__':
    unittest.main()
