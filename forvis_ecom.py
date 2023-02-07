import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from utils import p, quick_report

df = pd.read_csv(
    'ecom_clean.csv',
    parse_dates=['InvoiceDate'],
    dtype={'CustomerID': str, 'InvoiceID': str},
    index_col=False,
)


order_per_country = (
    df.groupby(['Country'])
    .size()
    .reset_index(name='count')
    .sort_values('count', ascending=False)
)
quick_report(order_per_country)


order_per_country.to_csv('order_per_country.csv', index=False)


customer_per_country = (
    df[['CustomerID', 'Country']]
    .drop_duplicates()
    .groupby(['Country'])
    .size()
    .reset_index(name='count')
    .sort_values('count', ascending=False)
)
quick_report(customer_per_country)


customer_per_country.to_csv('customer_per_country.csv', index=False)

order_by_date = df.groupby(['InvoiceDate']).size().reset_index(name='count')
# order_by_date = (
#     order_by_date.groupby(order_by_date['InvoiceDate'].dt.strftime('%m-%y'))
#     .agg(total=('count', 'sum'))
#     .reset_index()
# )
order_by_date['InvoiceDate'] = pd.to_datetime(
    order_by_date['InvoiceDate']
) - pd.to_timedelta(7, unit='d')
order_by_date = (
    order_by_date.groupby(pd.Grouper(key='InvoiceDate', freq='W-MON'))['count']
    .sum()
    .reset_index()
)
quick_report(order_by_date)


order_by_date.to_csv('order_by_date.csv', index=False)

order_by_date_country = (
    df.groupby(['InvoiceDate', 'Country']).size().reset_index(name='count')
)
# order_by_date_country = (
#     order_by_date_country.groupby(
#         [
#             order_by_date_country['InvoiceDate'].dt.strftime('%m-%y'),
#             order_by_date_country['Country'],
#         ]
#     )
#     .agg(total=('count', 'sum'))
#     .reset_index()
# )
order_by_date_country['InvoiceDate'] = pd.to_datetime(
    order_by_date_country['InvoiceDate'],
) - pd.to_timedelta(7, unit='d')
order_by_date_country = (
    order_by_date_country.groupby(
        [
            pd.Grouper(key='InvoiceDate', freq='W-MON'),
            'Country',
        ]
    )['count']
    .sum()
    .reset_index()
)
quick_report(order_by_date_country)


order_by_date_country.to_csv('order_by_date_country.csv', index=False)
