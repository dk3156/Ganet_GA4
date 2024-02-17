import streamlit as st
import pandas as pd
import plotly.express as px

#read
@st.cache_data
def load_data():
    df = pd.read_csv('ga_final.csv')
    df['date_format'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['start_time'] = pd.to_datetime(df['visitStartTime'], unit='s')
    return df

df = load_data()

def get_monthly():
    date_channel = df[['date_format', 'channelGrouping', 'fullVisitorId']]
    date_channel.columns = ['date', 'channelGrouping', 'fullVisitorId']
    year_month = date_channel['date'].dt.year.astype(str) + '-' + date_channel['date'].dt.month.astype(str)

    year_month = pd.DataFrame(year_month)
    date_channel = pd.concat([date_channel, year_month], axis=1)

    date_channel.columns = ['date', 'channelGrouping', 'fullVisitorId', 'monthly']
    mon_chan = pd.DataFrame(date_channel.groupby(['monthly', 'channelGrouping'])['fullVisitorId'].count())
    channel_1610 = mon_chan.loc['2016-10',].reset_index()
    channel_1611 = mon_chan.loc['2016-11',].reset_index()
    mon_chan = mon_chan.reset_index()
    return mon_chan, channel_1610, channel_1611
def monthly_bar_chart(mon_chan:pd.DataFrame):
    #draw
    fig = px.bar(mon_chan, x='monthly' , y='fullVisitorId', color='channelGrouping', barmode='group')
    fig.update_layout(xaxis_title='monthly', yaxis_title='visitors')
    st.plotly_chart(fig, use_container_width=True, height=600)
def pie_chart_one(channel_1610:pd.DataFrame):
    #draw
    fig = px.sunburst(channel_1610, path=['channelGrouping'], values='fullVisitorId')
    fig.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig, use_container_width=True, height=600)
def pie_chart_two(channel_1611:pd.DataFrame):
    #draw
    fig = px.sunburst(channel_1611, path=['channelGrouping'], values='fullVisitorId')
    fig.update_traces(textinfo="label+percent parent")
    st.plotly_chart(fig, use_container_width=True, height=600)

channel_groupings = get_monthly()

#titles  
st.set_page_config(
        page_icon="💎",
        page_title="팀 가넷 대시보드 💎",
        layout="wide",
)

cg = channel_groupings
st.subheader("월별 채널 유입 현황")
monthly_bar_chart(cg[0])

col2, col3 = st.columns([1, 1])
with col2:
    st.subheader("2016 10월 채널 유입")
    pie_chart_one(cg[1])
with col3:
    st.subheader("2016 11월 채널 유입")
    pie_chart_two(cg[2])