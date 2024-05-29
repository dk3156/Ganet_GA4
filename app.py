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
    df = pd.read_csv('df.csv')
    return df
df = load_data()
#draw
def mau_chart():
    #analyze
    date_df = pd.read_csv('date_df.csv')
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
    return st.plotly_chart(fig, use_container_width=True, height=400)
def cc_chart():
    res = pd.read_csv('res.csv')
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
    return st.plotly_chart(fig, use_container_width=True, height=400)
def ecdf_chart():
    ecdf = pd.read_csv('ecdf.csv')
    fig = px.ecdf(ecdf, x='max_min_minus')
    return st.plotly_chart(fig, use_container_width=True, height=400)
def retention_chart():
    retention = pd.read_csv('retention.csv')
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
    return st.plotly_chart(fig, use_container_width=True, height=600)

def avg_weekly_chart(start_week:str, end_week:str):
    week_count = pd.read_csv('week_count.csv')
    fig = px.imshow(week_count, 
                    color_continuous_scale='blues',
                    aspect='auto',
                    labels={'x': '요일', 'y': '시간'})
    return st.plotly_chart(fig, use_container_width=True, height=600)

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
