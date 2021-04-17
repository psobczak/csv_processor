from unittest.mock import patch, mock_open
import pytest
from csv_processor import CSVProcessor, CSVColumnException


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


@pytest.fixture
def simple_type_processor():
    return CSVProcessor("col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n", types=(int, int, int))


def test_sort_without_key(simple_type_processor):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    processor.sort()

    assert processor.csv == [[0, 5, 7], [1, 8, 3], [4, 5, 6]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_sort_without_key_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    processor.sort()

    assert processor.csv == [[0, "'str3'", 13.1], [1, "'str2'", 6.2], [2, "'str1'", 7.9]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_sort_with_key(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    processor.sort(key=1)

    assert processor.csv == [[4, 5, 6], [0, 5, 7], [1, 8, 3]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_sort_with_key_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    processor.sort(key=1)

    print(processor.csv)
    assert processor.csv == [[2, "'str1'", 7.9], [1, "'str2'", 6.2], [0, "'str3'", 13.1]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_top(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.top(2) == [[1, 8, 3], [4, 5, 6]]


def test_top_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor.top(2) == [[0, "'str3'", 13.1], [1, "'str2'", 6.2]]


def test_tail(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.tail(2) == [[4, 5, 6], [0, 5, 7]]


def test_tail_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor.tail(2) == [[1, "'str2'", 6.2], [2, "'str1'", 7.9]]


def test_get_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.get_column(2) == [3, 6, 7]


def test_get_column_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor.get_column(2) == [13.1, 6.2, 7.9]


def test_get_columns(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.get_columns((1, 2)) == [[8, 3], [5, 6], [5, 7]]


def test_get_columns_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor.get_columns((1, 2)) == [["'str3'", 13.1], ["'str2'", 6.2], ["'str1'", 7.9]]


def test_drop_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    processor.drop_column(2)
    assert processor.csv == [[1, 8], [4, 5], [0, 5]]


def test_drop_column_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    processor.drop_column(2)
    assert processor.csv == [[0, "'str3'"], [1, "'str2'"], [2, "'str1'"]]


def test_drop_columns(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))
    processor.drop_columns((0, 2))

    assert processor.csv == [[8], [5], [5]]
    assert processor.header == ['col2']


def test_drop_columns_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))
    processor.drop_columns((0, 1))

    assert processor.csv == [[13.1], [6.2], [7.9]]
    assert processor.header == ['col3']


def test_get_rows_by_column_value(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor.get_rows_by_column_value(1, 5) == [[4, 5, 6], [0, 5, 7]]
    assert processor.get_rows_by_column_value(1, 100) == []


def test_get_rows_by_column_value_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor.get_rows_by_column_value(0, 0) == [[0, "'str3'", 13.1]]
    assert processor.get_rows_by_column_value(0, 100) == []


def test_casting_to_str_and_back(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert CSVProcessor(str(processor), types=(int, int, int)) == processor


def test_indexing(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    assert processor[0::2] == [[1, 8, 3], [0, 5, 7]]


def test_indexing_multiple_types(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

    assert processor[0::2] == [[0, "'str3'", 13.1], [2, "'str1'", 7.9]]


def test_should_throw_when_column_out_of_bound(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=(int, int, int))

    with pytest.raises(CSVColumnException):
        processor.get_column(6)
        processor.get_column(-1)


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n")
def test_from_file(mock_file, simple_int_csv):
    path = 'path/to/file'

    processor_from_file = CSVProcessor.from_file(path)

    assert processor_from_file == CSVProcessor(simple_int_csv)
    mock_file.assert_called_once_with(path)


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2,col3\n0,'str3',13.1\n1,'str2',6.2\n2,'str1',7.9\n")
def test_from_file_multiple_types(mock_file, multiple_types_csv):
    path = 'path/to/file'

    processor_from_file = CSVProcessor.from_file(path)

    assert processor_from_file == CSVProcessor(multiple_types_csv)
    mock_file.assert_called_once_with(path)


def test_instances_with_same_headers_and_data_should_be_equal(simple_int_csv):
    processor1 = CSVProcessor(simple_int_csv)
    processor2 = CSVProcessor(simple_int_csv)

    assert processor1 == processor2


def test_instances_with_different_data_should_not_be_equal(multiple_types_csv, simple_int_csv):
    processor1 = CSVProcessor(simple_int_csv)
    processor2 = CSVProcessor(multiple_types_csv)

    assert processor1 != processor2

##################################
# Komentarz dot. użycia fixtures #
##################################
# Użycie fixtures w pliku 'test_csv_processor.py faktycznie nie jest zbyt optymalne, ponieważ obie fixtury zwracają
# jedynie surowy string reprezentujący plik .csv. Żaden z testów z tego jednak bezpośrednio nie korzysta, wszystkie
# testy korzystają z instancji klasy CSVProcessor.
# Lepszym rozwiązaniem było by utworzenie fixtur, które zwracają obiekty typu CSVProcessor, mogłyby one wyglądać tak:
#
# @pytest.fixture
# def multiple_types_processor():
#     return CSVProcessor("col1,col2,col3\n0,'str3',13.1\n1,'str2',6.2\n2,'str1',7.9\n", types=(int, str, float))
#
# @pytest.fixture
# def simple_int_processor():
#     return CSVProcessor("col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n", types=(int, int, int))
#
# Dzięki takiemu podejściu można by uniknąć duplikacji tych linii:
#  1.) processor = CSVProcessor(simple_int_csv, types=(int, int, int))
#  2.) processor = CSVProcessor(multiple_types_csv, types=(int, str, float))

# w prawie każdym teście. Wtedy metody testowe stały by się krótsze, oraz łatwiejsze do zrozumienia.
#
# Moglibyśmy przejść od tego:
# def test_top(simple_int_csv):
#     processor = CSVProcessor(simple_int_csv, types=(int, int, int))
#
#     assert processor.top(2) == [[1, 8, 3], [4, 5, 6]]
#
# Do tego:
# def test_top(simple_int_processor):
#     assert simple_int_processor.top(2) == [[1, 8, 3], [4, 5, 6]]
#
# co w skali całego modułu daje oszczędność kilkudziesięciu linii kodu
