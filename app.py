import streamlit as st 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

#titles  
st.set_page_config(
        page_icon="💎",
        page_title="팀 가넷 대시보드 💎",
        layout="wide",
    )
#페이지 헤더, 서브헤더
st.header('GA 데이터 분석 대시보드 💎')

#read
@st.cache_data
def load_data():
    df = pd.read_csv('ga_final.csv')
    df['date_format'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['start_time'] = pd.to_datetime(df['visitStartTime'], unit='s')
    return df
df = load_data()
#draw
@st.cache_data
def mau_chart():
    #analyze
    date_df = df[['fullVisitorId', 'date_format']]
    date_df['year'] = date_df['date_format'].dt.strftime('%Y')
    date_df['month'] = date_df['date_format'].dt.strftime('%m')
    date_df['week'] = date_df['date_format'].dt.isocalendar().week.astype(str)
    date_df['year_month'] = date_df['year'] + '-' + date_df['month']
    date_df['year_week'] = date_df['year'] + '-' + date_df['week']
    date_df['dau'] = date_df.groupby('date_format')['fullVisitorId'].transform('nunique')
    date_df['wau'] = date_df.groupby('year_week')['fullVisitorId'].transform('nunique')
    date_df['mau'] = date_df.groupby('year_month')['fullVisitorId'].transform('nunique')
    date_df = date_df.drop(columns=['fullVisitorId'])
    date_df = date_df.drop_duplicates()
    date_df = date_df.sort_values(by=['date_format'])
    #draw
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = date_df['date_format'], y = date_df['mau'], mode='lines', name='mau'))
    fig.add_trace(go.Scatter(x = date_df['date_format'], y = date_df['wau'], mode='lines', name='wau'))
    fig.add_trace(go.Scatter(x = date_df['date_format'], y = date_df['dau'], mode='lines', name='dau'))
    fig.update_layout(
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="right",
        legend_x=0.99
    )
    #show
    st.plotly_chart(fig, use_container_width=True, height=400)
@st.cache_data
def cc_chart():
    original = df[['date_format', 'fullVisitorId']]
    temp = original['date_format'].dt.year.astype(str) + '-' + original['date_format'].dt.month.astype(str)

    def get_semester(series):
        if series in ['2016-8', '2016-9']:
            return 1
        elif series in ['2016-10', '2016-11', '2016-12']:
            return 2
        elif series in ['2017-1', '2017-2', '2017-3']:
            return 3
        elif series in ['2017-4', '2017-5', '2017-6']:
            return 4
        elif series in ['2017-7', '2017-8']:
            return 5
        
    temp = pd.DataFrame(temp.apply(get_semester))
    # temp.groupby['date_format']['fullVisitorId'].apply(pd.DataFrame.nunique)
    original = pd.concat([original, temp], axis=1)
    original.columns = ['date_format', 'id', 'semester']

    customers_in_one = original[(original['semester'] == 1)]['id'].unique()
    customers_in_two = original[(original['semester'] == 2)]['id'].unique()
    customers_in_three = original[(original['semester'] == 3)]['id'].unique()
    customers_in_four = original[(original['semester'] == 4)]['id'].unique()
    customers_in_five = original[(original['semester'] == 5)]['id'].unique()

    # 1분기 신규
    one_new_user = len(customers_in_one)
    # 2분기 신규
    two_new_user = original[original['semester'] == 2][~original['id'].isin(customers_in_one)]['id'].nunique()
    # 3분기 신규
    three_new_user = original[original['semester'] == 3][~original['id'].isin(customers_in_one) &\
                                                        ~original['id'].isin(customers_in_two)]['id'].nunique()
    # 4분기 신규
    four_new_user = original[original['semester'] == 4][~original['id'].isin(customers_in_one) &\
                                                        ~original['id'].isin(customers_in_two) &\
                                                        ~original['id'].isin(customers_in_three)]['id'].nunique()
    # 5분기 신규
    five_new_user = original[original['semester'] == 5][~original['id'].isin(customers_in_one) &\
                                                        ~original['id'].isin(customers_in_two) &\
                                                        ~original['id'].isin(customers_in_three) &\
                                                        ~original['id'].isin(customers_in_four)]['id'].nunique()

    # 1분기 이탈
    one_churn_user = original[original['semester'] == 1][~original['id'].isin(customers_in_two) &\
                                                        ~original['id'].isin(customers_in_three) &\
                                                        ~original['id'].isin(customers_in_four) &\
                                                        ~original['id'].isin(customers_in_five)]['id'].nunique()
    # 2분기 이탈
    two_churn_user = original[original['semester'] == 2][~original['id'].isin(customers_in_three) &\
                                                        ~original['id'].isin(customers_in_four) &\
                                                        ~original['id'].isin(customers_in_five)]['id'].nunique()
    # 3분기 이탈
    three_churn_user = original[original['semester'] == 3][~original['id'].isin(customers_in_four) &\
                                                        ~original['id'].isin(customers_in_five)]['id'].nunique()
    # 4분기 이탈
    four_churn_user = original[original['semester'] == 4][~original['id'].isin(customers_in_five)]['id'].nunique()

    # 5분기 이탈 없음

    # 각 분기 유저수 
    sau_one = original[(original['semester'] == 1)]['id'].nunique()
    sau_two = original[(original['semester'] == 2)]['id'].nunique()
    sau_three = original[(original['semester'] == 3)]['id'].nunique()
    sau_four = original[(original['semester'] == 4)]['id'].nunique()

    # 각 분기 이탈률
    one_churn_rate = round(one_churn_user / sau_one, 2)
    two_churn_rate = round(two_churn_user / sau_two, 2)
    three_churn_rate = round(three_churn_user / sau_three, 2)
    four_churn_rate = round(four_churn_user / sau_four, 2)

    # 각 분기 cc 
    x_third_cc = one_new_user / one_churn_rate
    x_fourth_cc = two_new_user / two_churn_rate
    n_first_cc = three_new_user / three_churn_rate
    n_second_cc = four_new_user / four_churn_rate

    cc = {}
    cc['2016 삼분기'] = x_third_cc
    cc['2016 사분기'] = x_fourth_cc
    cc['2017 일분기'] = n_first_cc
    cc['2017 이분기'] = n_second_cc
    temp2 = pd.Series(cc)

    sau = {}

    sau['2016 삼분기'] = sau_one
    sau['2016 사분기'] = sau_two
    sau['2017 일분기'] = sau_three
    sau['2017 이분기'] = sau_four
    temp = pd.Series(sau)

    res = pd.concat([temp2, temp], axis=1).reset_index()
    res.columns = ['quarter', 'carrying capacity', 'qau']
    # draw
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = [res.loc[0, 'quarter'], res.loc[1, 'quarter'], res.loc[2, 'quarter'], res.loc[3, 'quarter']],
        y = [res.loc[0, 'carrying capacity'], res.loc[1, 'carrying capacity'], res.loc[2, 'carrying capacity'], res.loc[3, 'carrying capacity']],
        name = 'CC'
    ))
    fig.add_trace(go.Bar(
        x = [res.loc[0, 'quarter'], res.loc[1, 'quarter'], res.loc[2, 'quarter'], res.loc[3, 'quarter']],
        y = [res.loc[0, 'qau'], res.loc[1, 'qau'], res.loc[2, 'qau'], res.loc[3, 'qau']],
        name = 'QAU'
    ))
    fig.update_layout(
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="right",
        legend_x=0.99
    )
    st.plotly_chart(fig, use_container_width=True, height=400)
@st.cache_data
def ecdf_chart():
    from datetime import datetime
    train_df2 = df[['fullVisitorId', 'date_format', 'start_time']]
    train_df2.columns = ['fullVisitorId', 'date', 'start_time']
    group = train_df2.groupby(['date', 'fullVisitorId'])['start_time']

    result = pd.concat([group.min(), group.max()], axis=1)
    result.columns = ['min', 'max']
    result['min'] = result['min'].dt.strftime('%H:%M:%S')
    result['max'] = result['max'].dt.strftime('%H:%M:%S')
    
    result2 = result[result['max'] > result['min']]
    result2.reset_index(inplace=True)

    result2['min2'] = result2['min'].apply(lambda x: datetime.strptime(str(x), '%H:%M:%S'))
    result2['max2'] = result2['max'].apply(lambda x: datetime.strptime(str(x), '%H:%M:%S'))
    result2['max_min_minus'] = result2['max2'] - result2['min2']
    result2['max_min_minus'] = result2['max_min_minus'] / pd.Timedelta(1, 'h')
    id_max_min_minus_mean = pd.DataFrame(result2.groupby('fullVisitorId')['max_min_minus'].mean())
    total_max_min_minus_mean = result2['max_min_minus'].sum() / 47217

    ecdf = id_max_min_minus_mean / total_max_min_minus_mean
    ecdf.reset_index(inplace=True)

    fig = px.ecdf(ecdf, x='max_min_minus')
    st.plotly_chart(fig, use_container_width=True, height=400)
@st.cache_data
def retention_chart():
    week_df = df[['fullVisitorId', 'date_format', 'start_time']]
    week_df['year'] = week_df['date_format'].dt.isocalendar().year
    week_df['week'] = week_df['date_format'].dt.isocalendar().week
    week_df['current_week'] = week_df['year'] * 52 + week_df['week']
    index_lst = week_df['year'] + (week_df['week'] / 100)
    index_lst = sorted(list(index_lst.unique()))
    week_df['start_week'] = week_df.groupby(['fullVisitorId'])[['current_week']].transform('min')
    week_df['c_ind'] = week_df['current_week'] - week_df['start_week']
    week_df['start_week'] = week_df['start_week'] - week_df['start_week'].min()
    grouping = week_df.groupby(['start_week', 'c_ind'])
    cohort_data = grouping['fullVisitorId'].apply(pd.Series.nunique)
    cohort_data = pd.DataFrame(cohort_data)
    cohort_data = cohort_data.reset_index()
    cohort_counts = cohort_data.pivot(index='start_week', columns='c_ind', values='fullVisitorId')
    retention = cohort_counts
    indices = cohort_counts.index.to_list()
    column_inds = cohort_counts.columns.to_list()
    for i in range(len(indices)):
        m = indices[i]
        for j in range(len(column_inds)-1, 0, -1):
            retention.at[(m, column_inds[j])] = retention.at[(m, column_inds[j])] / retention.at[(m, column_inds[j-1])]
        retention.at[(m, 0)] = retention.at[(m, 0)] / retention.at[(m, 0)]
        
    #draw
    fig = px.imshow(retention, 
                zmin=0, 
                zmax=1, 
                color_continuous_scale='blues',
                labels={'x': 'cohort_index', 'y': 'start week'})
    fig.update_layout(
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="right",
        legend_x=0.99
    )
    st.plotly_chart(fig, use_container_width=True, height=600)
@st.cache_data
def avg_weekly_chart(start_week:str, end_week:str):
    # 전체 52주
    num_of_weeks = int((pd.to_datetime(end_week) - pd.to_datetime(start_week)) / np.timedelta64(1, 'W'))
    hourday = df[['fullVisitorId', 'date_format', 'start_time']]
    hourday['day'] = hourday['date_format'].dt.day_name()
    hourday['time'] = hourday['start_time'].dt.hour
    
    to_replace = [i for i in range(24)]
    value = []
    for i in range(24):
        if i == 0:
            value.append(f'12 am')
        elif 1 <= i < 12:
            value.append(f'{i} am')
        elif i == 12:
            value.append(f'12 pm')
        else:
            value.append(f'{i-12} pm')
            
    hourday['time'].replace(to_replace=to_replace, value=value, inplace=True)
    hourday = hourday[(hourday['date_format'] >= start_week) & (hourday['date_format'] <= end_week)]
    grouping = hourday.groupby(['day', 'time'])
    week_data = grouping['fullVisitorId'].apply(pd.Series.nunique)
    week_data = pd.DataFrame(week_data).divide(num_of_weeks).round(1)
    
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_data = week_data.reset_index()
    week_count = week_data.pivot(index='time', columns='day', values='fullVisitorId')
    week_count = week_count.reindex(columns=order)
    week_count = week_count.reindex(value)
    
    fig = px.imshow(week_count, 
                    color_continuous_scale='blues',
                    aspect='auto',
                    labels={'x': '요일', 'y': '시간'})
    st.plotly_chart(fig, use_container_width=True, height=600)

# 대시보드
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.subheader("DAU, WAU, MAU")
    mau_chart()

with col2:
    st.subheader("Carrying Capacity")
    cc_chart()

with col3:
    st.subheader("사용자 평균 접속 시간")
    ecdf_chart()
    
col3, col4 = st.columns([1, 1])
with col3:
    st.subheader("주간 리텐션")
    retention_chart()
with col4:
    st.subheader("요일/시간대별 유저수")
    avg_weekly_chart('2016-08-01', '2017-07-31')