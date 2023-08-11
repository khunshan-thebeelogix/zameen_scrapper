import csv
def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return
#Read the CSV file.
with open(r'C:\Users\CIS\Desktop\scraper\turkey_house_3.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(no_blank(csv_file))