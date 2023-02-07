from datetime import datetime

import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from utils import p, quick_report


def replace_with_thresholds(dataframe, variable, q1=0.25, q3=0.75):

    df_ = dataframe.copy()
    quartile1 = df_[variable].quantile(q1)
    quartile3 = df_[variable].quantile(q3)
    iqr = quartile3 - quartile1

    up_limit = quartile3 + 1.5 * iqr
    low_limit = quartile1 - 1.5 * iqr
    df_.loc[(df_[variable] < low_limit), variable] = low_limit
    df_.loc[(df_[variable] > up_limit), variable] = up_limit

    return df_


df = pd.read_csv(
    'ecom_clean.csv',
    parse_dates=['InvoiceDate'],
    dtype={'CustomerID': str, 'InvoiceID': str},
    index_col=False,
)
df = replace_with_thresholds(df, 'Quantity', q1=0.01, q3=0.99)
df = replace_with_thresholds(df, 'UnitPrice', q1=0.01, q3=0.99)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
p(df['InvoiceDate'].max())


df = df.groupby('CustomerID').agg(
    {
        'InvoiceDate': lambda x: (datetime(2011, 12, 11) - x.max()).days,
        'InvoiceNo': lambda x: x.nunique(),
        'TotalPrice': lambda x: x.sum(),
    }
)

df.columns = ['recency', 'frequency', 'monetary']
df = df[df['monetary'] > 0].reset_index()
df.drop(columns=['CustomerID'], inplace=True)
df['recency_score'] = pd.qcut(
    df['recency'],
    5,
    labels=[5, 4, 3, 2, 1],
)
df['frequency_score'] = pd.qcut(
    df['frequency'].rank(method='first'),
    5,
    labels=[1, 2, 3, 4, 5],
)
df['monetary_score'] = pd.qcut(
    df['monetary'],
    5,
    labels=[1, 2, 3, 4, 5],
)
df['RFM_SCORE'] = df['recency_score'].astype(str) + df['frequency_score'].astype(str)
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions',
}

df['segment'] = df['RFM_SCORE'].replace(seg_map, regex=True)
df = replace_with_thresholds(df, 'recency', q1=0.01, q3=0.99)
df = replace_with_thresholds(df, 'frequency', q1=0.01, q3=0.99)
df = replace_with_thresholds(df, 'monetary', q1=0.01, q3=0.99)

df.to_csv('rfm_ecom.csv')
quick_report(df)

seg = (
    df.groupby('segment')
    .size()
    .reset_index(name='count')
    .sort_values(by=['count'])
    .reset_index(drop=True)
)
seg.to_csv('segment_count.csv')
quick_report(seg)
