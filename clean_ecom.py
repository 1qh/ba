import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from utils import p, quick_report

df = pd.read_csv(
    'ecom.csv',
    encoding='unicode_escape',
    parse_dates=['InvoiceDate'],
    dtype={'CustomerID': str, 'InvoiceID': str},
    index_col=False,
)

quick_report(df)

p(df['Quantity'].min())
p(df['UnitPrice'].min())
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

df.drop_duplicates(inplace=True)
df.dropna(subset=['CustomerID'], inplace=True)
df['Description'] = df['Description'].str.lower()

quick_report(df)

df.to_csv('ecom_clean.csv', index=False)
