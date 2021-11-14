import pandas as pd
import urllib.request, json
import requests



# reading url
json_file = dict()
with urllib.request.urlopen("https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json") as url:
    json_file = json.loads(url.read().decode())

# Get data from json file
data = json_file["securities"]['data']
# Get columns' name from json file
cols = list((json_file["securities"]["columns"]))
print(cols)
# Create DataFrame from the data and the columns
df = pd.DataFrame(data, columns=cols, dtype=None, copy=False)
good_column = ['SECID', 'SHORTNAME', 'PREVWAPRICE', 'YIELDATPREVWAPRICE', 'COUPONVALUE', 'NEXTCOUPON', 'FACEVALUE',
                'ISIN', 'COUPONPERIOD', 'FACEUNIT', 'BUYBACKPRICE', 'LOTVALUE']

for column in cols:
    if not(column in good_column):
        df = df.drop(column, 1)

df = df.dropna()

unique_names = list(set(df['SHORTNAME'].tolist()))[0:10]
mask = df['SHORTNAME'].isin(unique_names)
df = df[mask]
df.to_csv('dataset.csv', encoding='utf-8')
