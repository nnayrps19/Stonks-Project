import unittest
import datasuite
import yfinance as yf
import pandas as pd
from os import remove

class TestTrader(unittest.TestCase):
    def setUp(self):
        #download data for testing
        temp = yf.download('FNGU', start='2021-1-1', end='2022-1-1')
        temp.to_json('tester.json', orient='index')
        self.example1 = pd.read_json('tester.json', precise_float=True, orient='index')

    def tearDown(self):
        remove('tester.json')
    
    def test_datasuite(self):
        #test read_data()
        datasuite.download('FNGU', start='2021-1-1', end='2022-1-1')
        data = pd.read_json('history.json', precise_float=True, orient='index')
        self.assertTrue(data.equals(datasuite.read_data()))

        #test download()
        self.assertTrue(data.equals(self.example1))

if __name__ == '__main__':
    unittest.main()
