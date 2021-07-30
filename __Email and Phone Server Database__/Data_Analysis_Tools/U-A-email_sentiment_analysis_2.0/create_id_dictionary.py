import pandas as pd
import csv

id_dict = {}

df = pd.read_excel('Fake Identities.xlsx')

ids = df['Profile ID#'].tolist()
emails = df['Email (@uaa.hume.vt.edu)'].tolist()

for index in range(len(ids)):
    id_dict[ids[index]] = emails[index].lower()

w = csv.writer(open("id_dict.csv", "w",newline=''))
for key, val in id_dict.items():
    w.writerow([key, val])