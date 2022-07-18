# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:40:06 2022

@author: HUANG Chun-Huang
"""

import sys
import os
dirname = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dirname)

import unittest

import pandas as pd

from ConfigTool.conf.IntersectionConfigurationHelper import IntersectionConfigurationHelper
from ConfigTool.conf.IntersectionConfiguration import IntersectionConfiguration

class IntersectionConfigurationHelperTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_columns(self):
        expected = ['name', 'version', 'date', 'intersection_id', 'road_type', 'road_num', 'link_id', 'name.1', 'lane_num', 'section', 'direction']
        result = IntersectionConfigurationHelper.columns()
        self.assertEqual(expected, result);

    def test_getEmptyInstance(self):
        expected = IntersectionConfiguration
        result = IntersectionConfigurationHelper.getEmptyInstance()
        result = (type(result) == IntersectionConfiguration)
        self.assertEqual(True, result)
    
if __name__ == "__main__":    
    suite = (unittest.TestLoader().loadTestsFromTestCase(IntersectionConfigurationHelperTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)    