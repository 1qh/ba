from pprint import pformat

import pandas as pd
import streamlit as st
from icecream import ic


def custom(o):
    return ('\n' + pformat(o, indent=2)).replace('\n', '\n' + 99 * '\b')


def dis(f, sidebar=False):
    if sidebar:
        st.sidebar.plotly_chart(
            f.update_layout(margin=dict(l=0, r=0, b=0, t=0), title_x=0, title_y=0.5),
            use_container_width=True,
        )
    else:
        st.plotly_chart(
            f.update_layout(margin=dict(l=0, r=0, b=0, t=0), title_x=0, title_y=0.5),
            use_container_width=True,
        )


def p(a):
    ic(a)


def num_or_not(df: pd.DataFrame):
    return (
        df.select_dtypes(include=['object']).columns.tolist(),
        df.select_dtypes(exclude=['object']).columns.tolist(),
    )


def quick_report(df):
    df.info()
    ic(df.duplicated().sum())
    ic(df.isna().sum())
    notnum, num = num_or_not(df)
    ic(notnum)
    ic(num)
    print('Unique values of every columns')
    ic(df.apply(lambda c: c.unique()))
    ic(df.apply(lambda c: c.unique().size))
    p(df)


ic.configureOutput(prefix='', argToStringFunction=custom)
