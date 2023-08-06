# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"path"


## import


import unittest


from op import fntime


## define


FN = "op.hdl.Event/2d390009cef944e68ce686e5709a54d7/2022-04-11/22:40:31.259218"


## class


class TestPath(unittest.TestCase):

    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)
