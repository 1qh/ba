import pandas as pd
import plotly.express as px
import streamlit as st

from utils import dis

st.set_page_config(layout='wide')
st.markdown(
    '''
<style>
footer {visibility: hidden;}
#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
# @font-face {font-family: 'SF Pro Display';}
# html, body, [class*='css']  {font-family: 'SF Pro Display';}
</style>
''',
    unsafe_allow_html=True,
)

page = st.sidebar.selectbox(
    'Select a page',
    (
        'Exploratory Data Analysis',
        'RFM Analysis',
    ),
)
if page == 'Exploratory Data Analysis':
    st.title('Exploratory Data Analysis')

    view = st.sidebar.selectbox(
        'Select a view',
        (
            'By time view',
            'By country view',
        ),
    )
    order_per_country = pd.read_csv('order_per_country.csv')
    customer_per_country = pd.read_csv('customer_per_country.csv')
    order_by_date_country = pd.read_csv('order_by_date_country.csv')
    order_cumsum_by_date_country = pd.read_csv('order_cumsum_by_date_country.csv')

    if view == 'By country view':
        st.header('By country view')

        tab1, tab2 = st.tabs(['Without UK', 'All countries'])
        with tab1:
            st.subheader('Number of customer per country')

            dis(
                px.pie(
                    customer_per_country[
                        customer_per_country['Country'] != 'United Kingdom'
                    ],
                    names='Country',
                    values='count',
                )
            )
            dis(
                px.choropleth(
                    customer_per_country[
                        customer_per_country['Country'] != 'United Kingdom'
                    ],
                    locationmode='country names',
                    locations='Country',
                    color='count',
                    color_continuous_scale='dense',
                )
            )
            st.subheader('Number of order per country')

            dis(
                px.pie(
                    order_per_country[order_per_country['Country'] != 'United Kingdom'],
                    names='Country',
                    values='count',
                )
            )
            dis(
                px.choropleth(
                    order_per_country[order_per_country['Country'] != 'United Kingdom'],
                    locationmode='country names',
                    locations='Country',
                    color='count',
                    color_continuous_scale='dense',
                )
            )
        with tab2:
            st.subheader('Number of customer per country')

            dis(
                px.pie(
                    customer_per_country,
                    names='Country',
                    values='count',
                )
            )
            dis(
                px.choropleth(
                    customer_per_country,
                    locationmode='country names',
                    locations='Country',
                    color='count',
                    color_continuous_scale='dense',
                )
            )
            st.subheader('Number of order per country')

            dis(
                px.pie(
                    order_per_country,
                    names='Country',
                    values='count',
                )
            )
            dis(
                px.choropleth(
                    order_per_country,
                    locationmode='country names',
                    locations='Country',
                    color='count',
                    color_continuous_scale='dense',
                )
            )
    if view == 'By time view':
        st.header('By time view')

        st.subheader('Number of orders by date')
        order_by_date = pd.read_csv('order_by_date.csv')

        dis(
            px.line(
                order_by_date,
                x='InvoiceDate',
                y='count',
                height=700,
                line_shape='spline',
            ).update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label='1m',
                                step='month',
                                stepmode='backward',
                            ),
                            dict(
                                count=3,
                                label='3m',
                                step='month',
                                stepmode='backward',
                            ),
                            dict(
                                count=6,
                                label='6m',
                                step='month',
                                stepmode='backward',
                            ),
                            dict(
                                count=1,
                                label='YTD',
                                step='year',
                                stepmode='todate',
                            ),
                            dict(
                                count=1,
                                label='1y',
                                step='year',
                                stepmode='backward',
                            ),
                            dict(step='all'),
                        ]
                    )
                ),
            )
        )

        st.subheader('Number of orders by date and country')
        tab1, tab2 = st.tabs(['Without UK', 'All countries'])
        with tab1:
            dis(
                px.bar(
                    order_cumsum_by_date_country[
                        order_cumsum_by_date_country['Country'] != 'United Kingdom'
                    ],
                    x='cumsum',
                    y='Country',
                    animation_frame='InvoiceDate',
                    height=1200,
                ).update_layout(yaxis={'categoryorder': 'total ascending'})
            )

            dis(
                px.line(
                    order_by_date_country[
                        order_by_date_country['Country'] != 'United Kingdom'
                    ],
                    x='InvoiceDate',
                    y='count',
                    color='Country',
                    height=700,
                    # line_shape='spline',
                ).update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list(
                            [
                                dict(
                                    count=1,
                                    label='1m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=3,
                                    label='3m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=6,
                                    label='6m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=1,
                                    label='YTD',
                                    step='year',
                                    stepmode='todate',
                                ),
                                dict(
                                    count=1,
                                    label='1y',
                                    step='year',
                                    stepmode='backward',
                                ),
                                dict(step='all'),
                            ]
                        )
                    ),
                )
            )
        with tab2:
            dis(
                px.bar(
                    order_cumsum_by_date_country,
                    x='cumsum',
                    y='Country',
                    animation_frame='InvoiceDate',
                    height=1000,
                ).update_layout(yaxis={'categoryorder': 'total ascending'})
            )

            dis(
                px.line(
                    order_by_date_country,
                    x='InvoiceDate',
                    y='count',
                    color='Country',
                    height=700,
                    # line_shape='spline',
                ).update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list(
                            [
                                dict(
                                    count=1,
                                    label='1m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=3,
                                    label='3m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=6,
                                    label='6m',
                                    step='month',
                                    stepmode='backward',
                                ),
                                dict(
                                    count=1,
                                    label='YTD',
                                    step='year',
                                    stepmode='todate',
                                ),
                                dict(
                                    count=1,
                                    label='1y',
                                    step='year',
                                    stepmode='backward',
                                ),
                                dict(step='all'),
                            ]
                        )
                    ),
                )
            )
if page == 'RFM Analysis':
    st.title('Recency Frequency Monetary Analysis')
    view = st.sidebar.selectbox(
        'Select a view',
        (
            'Segment Analysis',
            'Segmentation Map',
        ),
    )
    if view == 'Segmentation Map':
        st.subheader('Customer Segmentation Map by RFM scores')

        segment_count = pd.read_csv('segment_count.csv')

        dis(
            px.treemap(
                segment_count,
                path=['segment'],
                values='count',
                height=600,
            )
        )
        dis(
            px.pie(
                segment_count,
                values='count',
                names='segment',
            )
        )
    if view == 'Segment Analysis':
        st.header('Segment Analysis by RFM scores')

        rfm = pd.read_csv('rfm_ecom.csv')
        st.subheader('All 3 metrics w.r.t each other')
        dis(
            px.scatter_3d(
                rfm,
                x='recency',
                y='frequency',
                z='monetary',
                color='segment',
                height=700,
            ).update_traces(
                marker_size=2,
            )
        )
        st.subheader('Recency w.r.t Frequency')
        dis(
            px.scatter(
                rfm,
                x='recency',
                y='frequency',
                color='segment',
                height=700,
            )
        )
        for i in [
            'recency',
            'frequency',
            'monetary',
        ]:
            st.subheader(f'Distribution of {i.capitalize()} on each segment')
            dis(
                px.box(
                    rfm,
                    x=i,
                    y='segment',
                    height=700,
                )
            )
