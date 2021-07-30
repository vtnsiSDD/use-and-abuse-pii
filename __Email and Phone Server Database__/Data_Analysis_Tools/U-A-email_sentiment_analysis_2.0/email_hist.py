from datetime import datetime
import pandas as pd
import re
import matplotlib.pyplot as plt
import csv

reader = csv.reader(open('id_dict.csv', 'r'))
d = {}
for row in reader:
   k, v = row
   d[k] = v

quantity = {}

# Read in international Data
sheet_name = "email_data_one_sheet.xlsx"
df = pd.read_excel(sheet_name)
df_phone = df[df['From'].str.contains('zadarma')==True]
df = df[df['From'].str.contains('zadarma')==False]
to_list = df['To'].astype(str)
for rcp in to_list:
    unique_id = ''
    for k, v in d.items():
        if v in rcp:
            unique_id = int(k.split('_')[1])
    if unique_id in quantity.keys():
        quantity[unique_id] = quantity[unique_id] + 1
    else:
        quantity[unique_id] = 1

keys = list(quantity.keys())
keys = [str(key) for key in keys]
values = list(quantity.values())
num_emails = sum(values)
num_phone = len(df_phone.index)
#plt.bar(keys,values)
#plt.show()