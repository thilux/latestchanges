import unittest
import tempfile
import string
import random
import os
from latestchanges import get_latest_files, File

_TEMP_DIR = tempfile.mkdtemp()

def get_random_string(length):
    possible = list(string.ascii_letters) + list(string.digits)

    result = ''
    for _ in range(length):
        result += random.choice(possible)
    
    return result


def create_dummy_files(number_of_files=1, subdir=None):
    created_files = list()

    if subdir:
        os.makedirs(os.sep.join((_TEMP_DIR, subdir)))

    if number_of_files:
        for _ in range(number_of_files):
            directory = _TEMP_DIR + os.sep + subdir if subdir else _TEMP_DIR
            file_name = os.sep.join([directory, get_random_string(7)])
            file = open(file_name, 'w')
            file.close()
            created_files.append(file_name)
    return created_files


class LatestChanges(unittest.TestCase):

    def test_ordered_files(self):
        number_of_files = 5
        files = create_dummy_files(number_of_files)
        found_files = get_latest_files(source_dir=_TEMP_DIR)
        self.assertEqual(number_of_files, len(found_files))
        for x in range(number_of_files-1, -1, -1):
            self.assertEqual(files[x], found_files[number_of_files-x-1].file_name)

    def test_top_limit(self):
        number_of_files = 5
        top_limit = 2
        files = create_dummy_files(number_of_files)
        found_files = get_latest_files(top_limit=top_limit, source_dir=_TEMP_DIR)
        self.assertEqual(top_limit, len(found_files))
        self.assertEqual(files[-1], found_files[0].file_name)
        self.assertEqual(files[-2], found_files[1].file_name)

    def test_max_depth1(self):
        number_of_files = 5
        depth = 1
        files_depth1 = create_dummy_files(number_of_files=number_of_files)
        files_depth2 = create_dummy_files(number_of_files=number_of_files, subdir='subdir1')
        found_files = get_latest_files(source_dir=_TEMP_DIR, max_depth=depth)
        found_fnames = [f.file_name for f in found_files]
        for f in files_depth1:
            self.assertIn(f, found_fnames)

        for f in files_depth2:
            self.assertNotIn(f, found_fnames)

    def test_max_depth2(self):
        no_of_files = 5
        depth = 2
        files_depth1 = create_dummy_files(number_of_files=no_of_files)
        files_depth2 = create_dummy_files(number_of_files=no_of_files, subdir='subdir2')
        files_depth3 = create_dummy_files(number_of_files=no_of_files, subdir=os.sep.join(('subdir2', 'innersd1')))

        found_files = get_latest_files(source_dir=_TEMP_DIR, max_depth=depth)
        found_fnames = [f.file_name for f in found_files]
        for f in (files_depth1 + files_depth2):
            self.assertIn(f, found_fnames)

        for f in files_depth3:
            self.assertNotIn(f, found_fnames)

    def tearDown(self):
        for root, _, files in os.walk(_TEMP_DIR):
            for file in files:
                os.remove(root + os.sep + file)
