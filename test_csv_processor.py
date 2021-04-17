from unittest.mock import patch, mock_open
import pytest
from csv_processor import CSVProcessor


# TODO
# Uzupełnij ciała funkcji, które zawierają tylko `pass` (0.5pkt każda)
# Napisz testy analogiczne do tych już zaimplementowanych używając fixtury multiple_types_csv (0.5pkt każda)
# NB Punkty zostaną przyznane tylko, jeśli testowana metoda jest zaimplementowana
# Użycie fixtur w tym pliku jest trochę mało eleganckie i nie ogranicza duplikacji tak, jak powinno.
# Jeśli otrzymasz minimum 10pkt i napiszesz poniżej jak można lepiej wykorzystać możliwości fixtur w tym pliku
# to otrzymasz do 2pkt bonusu

@pytest.fixture
def simple_int_csv():
    return "col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n"


@pytest.fixture
def multiple_types_csv():
    return "col1,col2,col3\n0,'str3',13.1\n1,'str2',6.2\n2,'str1',7.9\n"


def test_sort_without_key(simple_int_csv):
    pass


def test_sort_with_key(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    processor.sort(key=1)

    assert processor.csv == [[4, 5, 6], [0, 5, 7], [1, 8, 3]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_top(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.top(2) == [[1, 8, 3], [4, 5, 6]]


def test_tail(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.tail(2) == [[4, 5, 6], [0, 5, 7]]


def test_get_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.get_column(2) == [3, 6, 7]


def test_get_columns(simple_int_csv):
    pass


def test_drop_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))
    processor.drop_column(1)

    assert processor.header == ["col1", "col3"]
    assert processor.csv == [[1, 3], [4, 6], [0, 7]]


def test_drop_columns(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))
    processor.drop_columns((0, 2))

    assert processor.csv == [[8], [5], [5]]
    assert processor.header == ['col2']


def test_get_rows_by_column_value(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.get_rows_by_column_value(1, 5) == [[4, 5, 6], [0, 5, 7]]


def test_casting_to_str_and_back(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert CSVProcessor(str(processor), types=(int, int, int)) == processor


def test_indexing(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor[0::2] == [[1, 8, 3], [0, 5, 7]]


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n")
def test_from_file(mock_file, simple_int_csv):
    path = 'path/to/file'

    processor_from_file = CSVProcessor.from_file(path)

    assert processor_from_file == CSVProcessor(simple_int_csv)
    mock_file.assert_called_once_with(path)


def test_instances_with_same_headers_and_data_should_be_equal(simple_int_csv):
    processor1 = CSVProcessor(simple_int_csv)
    processor2 = CSVProcessor(simple_int_csv)

    assert processor1 == processor2


def test_instances_with_different_data_should_not_be_equal(multiple_types_csv, simple_int_csv):
    processor1 = CSVProcessor(simple_int_csv)
    processor2 = CSVProcessor(multiple_types_csv)

    assert processor1 != processor2
