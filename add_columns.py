import csv
from datetime import datetime
import pandas as pd

todays_date = datetime.today().strftime('%Y-%m-%d')
# field_names = ['Scraping Date', 'Listing type', 'City', 'Province']

# with open(r"C:\Users\CIS\Desktop\scraper\zameen_Lahore2.csv","r") as fin, open("out1.csv", 'w', newline='') as fout:
    
#     reader = csv.reader(fin)
#     writer = csv.writer(fout)
#     write = csv.DictWriter(fout, fieldnames = field_names)
#     write.writeheader()
#     for line in reader:
#         line.append(todays_date)
#         line.append("House")
#         line.append("Lahore")
#         line.append("Punjab")
#         writer.writerow(line)

# df = pd.read_csv("sample.csv")
# df["new_column"] = ""
# df.to_csv("sample.csv", index=False)
df = pd.read_csv("zameen_Johar_Town_1.csv")
# df["Scraping date"] = todays_date
df["Listing Type"] = "House"
# df["City"] = "Attock"
# df["Province"] = "Punjab"
df['Week'] = "Week 1"
df['Place'] = "Johar Town"
df.to_csv("zameen_Johar_Town_2.csv", index=False)