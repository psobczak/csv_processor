class CSVProcessor:
    def __init__(self, csv: str, types=None, sep=','):
        split = [line.split(sep) for line in csv.splitlines()]
        self.header = split[0]
        self.csv = ([[type_(value) for (type_, value) in zip(types, values)] for values in split[1:]]
                    if types is not None else split[1:])

    def sort(self, key=None) -> None:
        if key is not None:
            key_index = self.header.index(key)
            print(key_index)

    def top(self, count: int) -> []:
        ...

    def bottom(self, count: int) -> []:
        ...

    def get_column(self, column: int) -> []:
        ...

    def get_columns(self, columns: [int]) -> [[]]:
        ...

    def drop_column(self, column: int) -> None:
        ...

    def drop_columns(self, columns: [int]) -> None:
        ...

    def get_rows_by_column_value(self, column: int, value: str) -> []:
        ...
