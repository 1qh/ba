from itertools import combinations, permutations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import scipy.cluster.hierarchy as sch
import seaborn as sns
import streamlit as st
from sklearn.cluster import DBSCAN, AffinityPropagation, AgglomerativeClustering, KMeans

from utils import dis, num_or_not


def num_hist(df):
    _, num = num_or_not(df)
    for i in num:
        st.subheader(f'{i.capitalize()} distribution')
        dis(
            px.histogram(
                df,
                i,
                marginal='box',
                height=600,
            )
        )


def num_violin(df):
    _, num = num_or_not(df)
    for i in num:
        st.subheader(f'{i.capitalize()} distribution')
        dis(
            px.violin(
                df,
                i,
                box=True,
                height=600,
            )
        )


def cate_pair_pie(df):
    cate, _ = num_or_not(df)

    for i in cate:
        st.sidebar.subheader(f'{i.capitalize()} distribution')
        dis(
            px.pie(
                df,
                i,
                title=i,
            ),
            sidebar=True,
        )

    for a, b in list(permutations(cate, 2)):
        for i in df[b].unique():
            dis(
                px.pie(
                    df[df[b] == i],
                    a,
                    title=f'{b}: {i}',
                    height=200,
                )
            )


def nume_cate_hist(df):
    cate, nume = num_or_not(df)
    for i in nume:
        for j in cate:
            st.subheader(f'{i.capitalize()} distribution by {j}')
            dis(
                px.histogram(
                    df,
                    x=i,
                    color=j,
                    barmode='group',
                    marginal='box',
                    height=700,
                )
            )


def nume_cate_violin(df):
    cate, nume = num_or_not(df)
    for i in nume:
        for j in cate:
            st.subheader(f'{i.capitalize()} distribution by {j}')
            dis(
                px.violin(
                    df,
                    x=i,
                    color=j,
                    box=True,
                    height=700,
                )
            )


def nume_pair_by_cate(df):
    cate, nume = num_or_not(df)
    for i in cate:
        for a, b in list(combinations(nume, 2)):
            st.subheader(f'{a.capitalize()} w.r.t {b} by {i}')
            dis(
                px.scatter(
                    df,
                    a,
                    b,
                    color=i,
                    trendline='ols',
                    color_discrete_sequence=['pink', 'green'],
                    height=700,
                ).update_traces(
                    marker_size=7,
                )
            )


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
df = pd.read_csv('mall_clean.csv')

page = st.sidebar.selectbox(
    'Select a page',
    (
        'Exploratory Data Analysis',
        'Customer Segmentation',
    ),
)
if page == 'Exploratory Data Analysis':
    st.title('Exploratory Data Analysis')

    view = st.sidebar.selectbox(
        'Select a view',
        (
            'Numerical',
            'Categorical',
        ),
    )
    if view == 'Categorical':
        kind = st.sidebar.selectbox(
            'Select chart type',
            (
                'Scatter Plot',
                'Distribution',
            ),
        )
        if kind == 'Distribution':
            cate_pair_pie(df)
            tab1, tab2 = st.tabs(['Histogram', 'Violin Chart'])
            with tab1:
                nume_cate_hist(df)
            with tab2:
                nume_cate_violin(df)
        if kind == 'Scatter Plot':
            dis(
                px.scatter_3d(
                    df,
                    'age',
                    'income',
                    'score',
                    color='gender',
                    color_discrete_sequence=['pink', 'green'],
                    height=700,
                ).update_traces(
                    marker_size=3,
                )
            )
            nume_pair_by_cate(df)

    if view == 'Numerical':
        st.sidebar.subheader('Correlation Matrix')
        corr = df.corr(numeric_only=True)
        fig = plt.figure(figsize=(3, 2))
        sns.heatmap(corr.iloc[1:, :-1], annot=True, mask=np.triu(corr)[1:, :-1])
        st.sidebar.pyplot(fig)

        tab1, tab2 = st.tabs(['Histogram', 'Violin Chart'])
        with tab1:
            num_hist(df)
        with tab2:
            num_violin(df)

if page == 'Customer Segmentation':
    clus = df.drop(columns=['gender'])
    st.title('Customer Segmentation')

    algo = st.sidebar.selectbox(
        'Select a algorithm',
        (
            'K-Means',
            'Hierarchical',
            'Affinity Propagation',
            'DBSCAN',
        ),
    )
    if algo == 'K-Means':
        k = st.sidebar.slider('Number of clusters', 2, 10, 5)
        st.header('K-Means')
        st.subheader('Within-Cluster Sums of Squares vs Number of Clusters')
        wcss = []
        for i in range(1, 11):
            model = KMeans(
                n_clusters=i,
                init='k-means++',
                max_iter=500,
                n_init=10,
                random_state=123,
            ).fit(clus)
            wcss.append(model.inertia_)

        dis(
            px.line(
                x=range(1, 11),
                y=wcss,
                line_shape='spline',
                height=700,
            ).update_layout(
                xaxis_title='Clusters',
                yaxis_title='WCSS',
            )
        )

        kmeans = df.copy()
        kmeans['cluster'] = (
            KMeans(
                n_clusters=k,
                init='k-means++',
                max_iter=500,
                n_init=10,
                random_state=123,
            )
            .fit_predict(clus)
            .astype(str)
        )
        kmeans.sort_values(by='cluster', inplace=True)
        dis(
            px.scatter_3d(
                kmeans,
                'age',
                'income',
                'score',
                color='cluster',
                height=700,
            ).update_traces(
                marker_size=6,
            )
        )
    if algo == 'Hierarchical':
        k = st.sidebar.slider('Number of clusters', 2, 10, 5)
        st.header('Hierarchical Clustering')
        st.subheader('Dendrogram')
        dis(
            ff.create_dendrogram(
                clus,
                linkagefun=lambda x: sch.linkage(x, 'ward'),
            ).update_layout(
                xaxis_title='Customers',
                yaxis_title='Euclidean Distance',
                height=700,
            )
        )
        hier = df.copy()
        hier['cluster'] = (
            AgglomerativeClustering(
                n_clusters=k,
                metric='euclidean',
                linkage='ward',
            )
            .fit_predict(clus)
            .astype(str)
        )
        hier.sort_values(
            by='cluster',
            inplace=True,
        )
        dis(
            px.scatter_3d(
                hier,
                'age',
                'income',
                'score',
                color='cluster',
                height=700,
            ).update_traces(
                marker_size=6,
            )
        )
    if algo == 'Affinity Propagation':
        st.header('Affinity Propagation')
        ap = df.copy()
        ap['cluster'] = AffinityPropagation(
            random_state=0,
        ).fit_predict(clus)
        ap.sort_values(
            by='cluster',
            inplace=True,
        )
        ap['cluster'] = ap['cluster'].astype(str)
        dis(
            px.scatter_3d(
                ap,
                'age',
                'income',
                'score',
                color='cluster',
                height=700,
            ).update_traces(
                marker_size=6,
            )
        )
    if algo == 'DBSCAN':
        st.header('DBSCAN')
        db = df.copy()
        db['cluster'] = DBSCAN(
            eps=9,
            min_samples=5,
        ).fit_predict(clus)
        db.sort_values(
            by='cluster',
            inplace=True,
        )
        db['cluster'] = db['cluster'].astype(str)
        dis(
            px.scatter_3d(
                db,
                'age',
                'income',
                'score',
                color='cluster',
                height=700,
            ).update_traces(
                marker_size=6,
            )
        )
