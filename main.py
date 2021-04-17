from csv_processor import CSVProcessor

if __name__ == '__main__':
    csv_lines = ""
    with open('test.csv', 'r') as file:
        csv = CSVProcessor(file.read())

        print(csv.csv)
        csv.sort(0)
        print(csv.csv)
