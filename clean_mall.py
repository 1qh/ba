import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from utils import quick_report

df = (
    pd.read_csv(
        'mall.csv',
        index_col=False,
    )
    .drop(columns=['CustomerID'])
    .sort_values(by=['Age'])
)

df.columns = [
    'gender',
    'age',
    'income',
    'score',
]
df.to_csv('mall_clean.csv', index=False)

quick_report(df)
