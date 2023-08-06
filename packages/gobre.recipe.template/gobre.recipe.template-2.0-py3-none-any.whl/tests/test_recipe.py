import os
import unittest
import zc.buildout.buildout


class TemplateTest(unittest.TestCase):

    def setUp(self):
        pass

    def default(self, test_name):
        zc.buildout.buildout.main(["-o", "install", test_name])

        f = open("test.out")
        self.assertEqual("root\n", f.read())

    def test_simple(self):
        self.default('simple-test')

    def test_filter(self):
        zc.buildout.buildout.main(["-o", "install", "filter-test"])

        f = open("test.out")

        self.assertEqual('    "root",\n    "toor"\n', f.read())

    def test_this(self):
        self.default('this-test')

    def test_dashed(self):
        self.default('dashed-test')

    def test_readme(self):
        zc.buildout.buildout.main(["-o", "install", "readme-test"])
        f = open("test.out")

        self.assertEqual('borg\ncash\nMe\n', f.read())

    def tearDown(self):
        try:
            os.remove("test.out")
        except:  # noqa: E722 do not use bare 'except'
            pass
