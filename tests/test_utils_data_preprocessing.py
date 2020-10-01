"""
Trading-Technical-Indicators (tti) python library

File name: test_utils_data_preprocessing.py
    tti.utils package, data_preprocessing.py module unit tests.
"""

import unittest
import pandas as pd

from tti.utils import data_preprocessing as dp


class TestFillMissingValues(unittest.TestCase):

    def test_input_parameter_missing(self):
        with self.assertRaises(TypeError):
            dp.fillMissingValues()

    def test_input_parameter_wrong_type(self):
        with self.assertRaises(TypeError):
            self.assertEqual(dp.fillMissingValues(1), 1)

    def test_input_parameter_empty_dataframe(self):
        df = pd.DataFrame(index=range(10), columns=['A'], data=None,
                          dtype=float)

        pd.testing.assert_frame_equal(dp.fillMissingValues(df), df)

    def test_result_sorted_input(self):
        df = pd.DataFrame(index=range(10), columns=['A'],
                          data=[None, None, 3., 4., None, None, 7., 8., 9.,
                                None])

        df_res = pd.DataFrame(index=range(10), columns=['A'],
                              data=[3., 3., 3., 4., 4., 4., 7., 8., 9., 9.])

        pd.testing.assert_frame_equal(dp.fillMissingValues(df), df_res)

    def test_result_not_sorted_input(self):
        df = pd.DataFrame(index=[3, 4, 2, 1, 5, 6, 7, 9, 8, 0], columns=['A'],
                          data=[None, None, 3., 4., None, None, 7., 8., 9.,
                                None])

        df_res = pd.DataFrame(index=range(10), columns=['A'],
                              data=[4., 4., 3., 3., 3., 3., 3., 7., 9., 8.])

        pd.testing.assert_frame_equal(dp.fillMissingValues(df), df_res)

    def test_result_input_multiple_columns(self):
        df = pd.DataFrame(index=range(5), columns=['A', 'B', 'C'],
                          data=[[None, 0., 0.], [1., None, 1.], [2., None, 2.],
                                [3., 3., None], [4., 4., None]])

        df_res = pd.DataFrame(index=range(5), columns=['A', 'B', 'C'],
                              data=[[1., 0., 0.], [1., 0., 1.], [2., 0., 2.],
                                    [3., 3., 2.],
                                    [4., 4., 2.]])

        pd.testing.assert_frame_equal(dp.fillMissingValues(df), df_res)

    def test_all_possible_missing_places(self):
        df_input = pd.read_csv('./data/missing_values_data.csv',
                               parse_dates=True, index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True, index_col=0)

        pd.testing.assert_frame_equal(dp.fillMissingValues(df_input),
                                      df_expected_result)


if __name__ == '__main__':
    unittest.main()
