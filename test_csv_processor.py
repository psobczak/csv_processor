import unittest
from csv_processor import CSVProcessor

csv_lines = ""
with open('test.csv', 'r') as file:
    csv = CSVProcessor(file.read())


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, False)

    def test_sort_should_sort_rows_by_key(self):
        ...

if __name__ == '__main__':
    unittest.main()
