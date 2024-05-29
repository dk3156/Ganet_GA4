import streamlit as st
import pandas as pd
import plotly.express as px

#titles  
st.set_page_config(
        page_icon="💎",
        page_title="팀 가넷 대시보드 💎",
        layout="wide",
    )
#read
@st.cache_data
def load_data():
    df = pd.read_csv('df.csv')
    return df
df = load_data()

# @st.cache_data
def monthly_bar_chart():
    #draw
    mon_chan = pd.read_csv('mon_chan.csv')
    fig = px.bar(mon_chan, x='monthly' , y='fullVisitorId', color='channelGrouping', barmode='group')
    fig.update_layout(xaxis_title='monthly', yaxis_title='visitors')
    st.plotly_chart(fig, use_container_width=True, height=600)
# @st.cache_data
def pie_chart_one():
    #draw
    channel_1610 = pd.read_csv('1610.csv')
    fig = px.sunburst(channel_1610, path=['channelGrouping'], values='fullVisitorId')
    fig.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig, use_container_width=True, height=600)
# @st.cache_data
def pie_chart_two():
    #draw
    channel_1611 = pd.read_csv('1611.csv')
    fig = px.sunburst(channel_1611, path=['channelGrouping'], values='fullVisitorId')
    fig.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig, use_container_width=True, height=600)


st.subheader("월별 채널 유입 현황")
monthly_bar_chart()

col2, col3 = st.columns([1, 1])
with col2:
    st.subheader("2016 10월 채널 유입")
    pie_chart_one()
with col3:
    st.subheader("2016 11월 채널 유입")
    pie_chart_two()
