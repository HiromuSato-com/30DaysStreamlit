# -*- coding: utf-8 -*-
"""
Spyderエディタ
Created on 07/04/2024
@author: Hiromu Sato
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
import datetime as dt

# define functions

def style_negative(v, props=''):
    """ Style negative values in dataframe """
    try:
        return props if v < 0 else None
    except:
        pass
def style_positive(v, props=''):
    """ Style positive values in dataframe """
    try:
        return props if v > 0 else None
    except:
        pass

# load data
def load_data():
    # Skip first raw
    df_agg = pd.read_csv('Aggregated_Metrics_By_Video.csv').iloc[1:,:]
    df_agg.columns = ['Video','Video title','Video publish time','Comments added',
                      'Shares','Dislikes','Likes','Subscribers lost','Subscribers gained',
                      'RPM (USD)','CPM (USD)','Average percentage viewed (%)','Average view duration',
                      'Views','Watch time (hours)','Subscribers','Your estimated revenue (USD)',
                      'Impressions','Impressions ctr (%)'
                      ]
    df_agg['Video publish time'] = pd.to_datetime(df_agg['Video publish time'],format='mixed')
    df_agg['Average view duration'] = df_agg['Average view duration'].apply(lambda x: datetime.strptime(x,"%H:%M:%S"))
    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    df_agg['Engagement_ratio'] = (df_agg['Comments added'] + df_agg['Shares'] + df_agg['Dislikes'] + df_agg['Likes']) / df_agg.Views
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']
    df_agg_sub = pd.read_csv('Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments = pd.read_csv('ALL_Comments_Final.csv')
    df_time = pd.read_csv('Video_Performance_Over_Time.csv')
    df_time['Date'] = pd.to_datetime(df_time['Date'],format='mixed')
    return df_agg, df_agg_sub,df_comments,df_time

df_agg, df_agg_sub, df_comments, df_time = load_data()
# engineer data
df_agg_diff = df_agg.copy()
metric_Data_12mo = df_agg_diff['Video publish time'].max() - pd.DateOffset(months =12)
filtering_agg = df_agg_diff[df_agg_diff['Video publish time'] >= metric_Data_12mo]
#median_agg = filtering_agg.median()
median_agg = filtering_agg.loc[:,list(filtering_agg.columns[3:12])+list(filtering_agg.columns[12:])].median()

numeric_cols = np.array((df_agg_diff.dtypes == 'float64') | (df_agg_diff.dtypes == 'int64'))
#numeric_cols = numeric_cols.loc[list(numeric_cols.rows[3:12])+list(numeric_cols.rows[12:]),:]
df_agg_diff.iloc[:,numeric_cols] = (df_agg_diff.iloc[:,numeric_cols] - median_agg).div(median_agg)


df_time_diff = pd.merge(df_time, df_agg.loc[:,['Video','Video publish time']],left_on='External Video ID',right_on=)



# build dashboard
add_sidebar = st.sidebar.selectbox('Aggregate or Indivisual Videos',('Aggregate Metrics','Indivisual Video Anaysis'))
## Total pictures
if add_sidebar == 'Aggregate Metrics':
    df_agg_metrics = df_agg[['Video','Video title','Video publish time','Comments added',
                             'Shares','Dislikes','Likes','Subscribers lost','Subscribers gained',
                             'RPM (USD)','CPM (USD)','Average percentage viewed (%)','Average view duration',
                             'Views','Watch time (hours)','Subscribers','Your estimated revenue (USD)',
                             'Impressions','Impressions ctr (%)',
                             'Avg_duration_sec','Engagement_ratio','Views / sub gained']]
    #df_agg_metrics_diff = df_agg_metrics.copy()
    metric_data_6mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months =6)
    metric_data_12mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months =12)
    metric_medians6mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_data_6mo]
    metric_medians6mo = metric_medians6mo.loc[:,list(metric_medians6mo.columns[3:12])+list(metric_medians6mo.columns[12:])].median()
    metric_medians12mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_data_12mo]
    metric_medians12mo = metric_medians12mo.loc[:,list(metric_medians12mo.columns[3:12])+list(metric_medians12mo.columns[12:])].median()
    
    #st.metric('Views',metric_medians6mo['Views'],500)
    # represent by loop
    col1,col2,col3,col4,col5 = st.columns(5)
    colums = [col1,col2,col3,col4,col5]
    count = 0
    for i in metric_medians6mo.index:
        with colums[count]:
            if pd.api.types.is_numeric_dtype(metric_medians6mo[i]) and pd.api.types.is_numeric_dtype(metric_medians12mo[i]):
                # print("Type:",pd.api.types.is_numeric_dtype(metric_medians12mo[i]))
                #delta = (metric_medians6mo[i] - metric_medians12mo[i])
                delta = dt.timedelta(metric_medians6mo[i] - metric_medians12mo[i])/(dt.timedelta(metric_medians12mo[i]))
                #print("type delta",pd.api.types.is_numeric_dtype(delta))
            print(f"Delta for {i}: {delta}")
            value = metric_medians6mo[i]
            if isinstance(value, (int, float, np.number)):
                st.metric(label=i, value=round(value, 1), delta='{:.2%}'.format(delta))
            else:
                st.metric(label=i, value=str(value), delta='{:.2%}'.format(delta))
            count += 1
            if count >= 5:
                count = 0
    
    #df_agg_diff['Publish_date'] = df_agg_diff['Video publish time'].apply(lambda x: x.date())
    df_agg_diff_final = df_agg_diff.loc[:,['Video publish time','Comments added',
                                           'Shares','Dislikes','Likes','Subscribers lost','Subscribers gained',
                                           'RPM (USD)','CPM (USD)','Average percentage viewed (%)',
                                           'Views','Watch time (hours)','Subscribers','Your estimated revenue (USD)',
                                           'Impressions','Impressions ctr (%)',
                                           'Avg_duration_sec','Engagement_ratio','Views / sub gained']]
    
    df_agg_diff_lst = df_agg_diff_final.median().index.tolist()
    df_to_pct = {}
    for i in df_agg_diff_lst:
        df_to_pct[i] = '{:.1%}'.format
    
    st.dataframe(df_agg_diff_final.style.hide().map(style_negative,props='color:red;').map(style_positive,props='color:green;'))
if add_sidebar == 'Indivisual Video Analysis':
    videos = tuple(df_agg['Video title'])
    video_select = st.selectbox('Pick A Video:',videos)
    
    agg_filtered = df_agg[df_agg['Video Title'] == video_select]
    agg_sub_filtered = df_agg_sub[df_agg_sub['Video Title'] == video_select]
    agg_sub_filtered['Country'] = agg_sub_filtered['Country Code'].apply(audience_simple)
    agg_sub_filtered.sort_values('Is Subscribed',inplace= True)
    
    fig = px.bar(agg_sub_filtered, x = 'Views', y = 'Is Subscribed', color = 'Country',orientation='h')
    st.plotly_chart(fig)
    
    agg_time_filtered = df_time_diff[df_time_diff['Video Title'] == video_select]
    first_30 = agg_time_filtered[agg_time_filtered['days_published'].between(0,30)]
    first_30 = first_30.sort_values('days_published')
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=views_cumulative['days_published'],y=views_cumulative['20pct_views'],
                              mode='lines',
                              name='20th percentile',line=dict(color='purple',dash='dash')))







