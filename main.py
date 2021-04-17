from csv_processor import CSVProcessor

if __name__ == '__main__':
    with open('sample.csv') as file:
        csv = CSVProcessor(file.read(), types=(int, str, str, int))


    print(csv.csv)

