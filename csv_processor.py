# TODO
# Zaimplementuj metody o nazwach i parametrach z komentarzy (1pkt każda), jeśli nazwa metody nie jest podana,
# to należy zaimplementować jedną z magic/dunder methods
# https://docs.python.org/3/reference/datamodel.html#basic-customization

# Do wybranej metody przyjmującej indeks kolumny dopisz walidację, która sprawdzi, czy podany indeks
# nie przekracza rozmiaru CSV, jeśli tak, to rzuć stworzonym przez siebie wyjątkiem (1.5pkt),
# dopisz sprawdzający to test (0.5pkt)

# Jeśli otrzymasz minimum 10pkt, a oba pliki (csv_processor.py i test_csv_processor.py) pozytwynie przejdą
# walidację przy użyciu komendy `flake8 --max-line-length=120`, to otrzymasz dodatkowe 2 punkty bonusu

class CSVProcessor:
    def __init__(self, csv: str, types=None, sep=','):
        split = [line.split(sep) for line in csv.splitlines()]
        self.header = split[0]
        self.csv = ([[type_(value) for (type_, value) in zip(types, values)] for values in split[1:]]
                    if types is not None else split[1:])

    def __getitem__(self, item):
        return self.csv[item]

    def __eq__(self, other):
        if not isinstance(other, CSVProcessor):
            return False
        return self.header == other.header and self.csv == other.csv

    # `sort` - sortuje wiersze, opcjonalny argument `key`, oznacza kolumnę, według której należy sortować
    # NB tutaj i niżej - nagłówek nie jest liczony jako wiersz
    def sort(self, key=None) -> None:
        sorted(self.csv, key=lambda row: row[key])

    # `top` - zwraca `count` pierwszych wierszy
    def top(self, count: int) -> [[]]:
        return self.csv[:count]

    # `top` - zwraca `count` ostatnich wierszy
    def tail(self, count: int) -> [[]]:
        return self.csv[-count:]

    # `get_column` - zwraca listę wszystkich wartości z kolumny o indeksie `column`
    def get_column(self, column: int) -> []:
        return [value[column] for value in self.csv]

    # `get_columns` - zwraca listę list wartości z kolumn o indeksach `columns`
    def get_columns(self, columns: [int]) -> [[]]:
        return [row[columns] for row in self.csv]

    # `drop_column` - usuwa kolumnę o indeksie `column` z CSV
    def drop_column(self, column: int) -> None:
        del self.header[column]
        for row in self.csv:
            del row[column]

    # `drop_columns` - usuwa kolumny o indeksach `columns` z CSV
    def drop_columns(self, columns: [int]) -> None:
        headers = self.header

        for row in self.csv:
            for index in columns:
                del row[index]

    # `get_rows_by_column_value` - zwraca wszystkie wiersze, które w kolumnie `column` mają wartość `value`
    def get_rows_by_column_value(self, column: int, value: str) -> [[]]:
        return [row for row in self.csv if row[column] == value]

    # Obiekt klasy CSVProcessor ma dać zamienić się na obiekt klasy str poprawnie reprezentujący zawartość pliku CSV

    # CSVProcessor(data)[n] powinno zwracać n-ty wiersz pilku

    # Dwa różne obiekty klasy CSVProcessor powinno dać się porównać przy użyciu `==`, są one równe, jeśli mają takie
    # same nagłówki i dane (z uwzględnieniem typów)

    # `from_file` przyjmuje ścieżkę do pliku `path` i zwraca obiekt klasy CSVProcessor stworzony z jego zawartości
    # `from_file` to classmethod https://docs.python.org/3/library/functions.html#classmethod

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as file:
            return cls(file.read())
