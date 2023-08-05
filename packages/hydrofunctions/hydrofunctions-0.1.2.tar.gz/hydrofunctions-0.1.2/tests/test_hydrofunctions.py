#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hydrofunctions
----------------------------------

Tests for `hydrofunctions` module.
"""
from __future__ import absolute_import, print_function
from unittest import mock
import unittest

import pandas as pd

from hydrofunctions import hydrofunctions as hf


class TestHydrofunctions(unittest.TestCase):

    @mock.patch('requests.get')
    def test_get_nwis_calls_correct_url(self, mock_get):

        """
        Thanks to
        http://engineroom.trackmaven.com/blog/making-a-mockery-of-python/
        """

        site = 'A'
        service = 'B'
        start = 'C'
        end = 'D'

        expected_url = 'http://waterservices.usgs.gov/nwis/B/?'
        expected_headers = {'max-age': '120', 'Accept-encoding': 'gzip'}
        expected_params = {'format': 'json,1.1', 'sites': 'A', 'endDT': 'D',
                           'startDT': 'C', 'parameterCd': '00060'}
        expected = 'mock data'

        mock_get.return_value = expected
        actual = hf.get_nwis(site, service, start, end)
        mock_get.assert_called_once_with(expected_url, params=expected_params,
                                         headers=expected_headers)
        self.assertEqual(actual, expected)

    def test_extract_nwis_dict(self):
        # I need to make a response fixture to test this out!!
        test = hf.get_nwis("01589440", "dv", "2013-01-01", "2013-01-05")
        actual = hf.extract_nwis_dict(test)
        self.assertIs(type(actual), dict, msg="Did not return a dict")

    def test_extract_nwis_df(self):
        # I need to make a response fixture to test this out!!
        test = hf.get_nwis("01589440", "dv", "2013-01-01", "2013-01-05")
        actual = hf.extract_nwis_df(test)
        self.assertIs(type(actual), pd.core.frame.DataFrame,
                      msg="Did not return a df")


if __name__ == '__main__':
    unittest.main(verbosity=2)
