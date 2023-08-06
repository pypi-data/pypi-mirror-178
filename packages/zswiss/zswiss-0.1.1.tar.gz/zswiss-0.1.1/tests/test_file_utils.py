import unittest
from zswiss.utils.file_utils import load_to_set
from zswiss.utils.file_utils import load_to_list


class TestFileUtils(unittest.TestCase):

    def test_load_to_list(self):
        paths = ['../docs/samples']
        res = load_to_list(paths, deduplicate=True, appendix=None)
        self.assertListEqual(res, ['2.txt', '1.txt'], 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_list(paths, deduplicate=True, appendix='txt')
        self.assertListEqual(res, ['11.txt', '21.txt', '1.txt', '2.txt'], 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_list(paths, deduplicate=False, appendix='txt')
        self.assertListEqual(res, ['11.txt', '11.txt', '21.txt', '1.txt', '2.txt'], 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_list(paths, deduplicate=False, appendix=None)
        self.assertSetEqual(set(res), set(['11.txt', '11.txt', '12', '21.txt', '21', '1.txt', '2.txt']), 'error')

        paths = ['../docs/samples']
        res = load_to_list(paths, appendix=None, recurse=True)
        print('res:', res)
        self.assertSetEqual(set(res), set(['11.txt', '12', '21', '21.txt', '1.txt', '2.txt']))

    def test_load_to_set(self):
        paths = ['../docs/samples']
        res = load_to_set(paths, appendix=None)
        self.assertSetEqual(res, set(['2.txt', '1.txt']), 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_set(paths, appendix='txt')
        self.assertSetEqual(res, set(['11.txt', '21.txt', '1.txt', '2.txt']), 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_set(paths, appendix='txt')
        self.assertSetEqual(res, set(['11.txt', '11.txt', '21.txt', '1.txt', '2.txt']), 'error')

        paths = ['../docs/samples/subdir1', '../docs/samples/subdir2', '../docs/samples/1.txt', '../docs/samples/2.txt']
        res = load_to_set(paths, appendix=None)
        self.assertSetEqual(set(res), set(['11.txt', '11.txt', '12', '21.txt', '21', '1.txt', '2.txt']), 'error')

        paths = ['../docs/samples']
        res = load_to_set(paths, appendix=None, recurse=True)
        self.assertSetEqual(set(res), set(['11.txt', '12', '21', '21.txt', '1.txt', '2.txt']))


if __name__ == '__main__':
    unittest.main()
