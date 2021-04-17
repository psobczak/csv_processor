from csv_processor import CSVProcessor

if __name__ == '__main__':
    csv = CSVProcessor.from_file('sample.csv', types=(int, str, str, int))
    print(csv.csv)
    print(csv.get_column(1))
