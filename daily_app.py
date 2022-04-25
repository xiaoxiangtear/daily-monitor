## streamlit主程序
import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import time
tt = time.time()

## >>>>> 初始设置 <<<<<
st.set_page_config(
     page_title="daily-monitor",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)


## 处理数据
@st.cache(allow_output_mutation=True)
def getData():

    conn = sqlite3.connect('daily.db')


    close_df = pd.read_sql('select * from `close`', con=conn)
    ps_df = pd.read_sql('select * from `ps`', con=conn)
    ps_df = ps_df[(ps_df['值']>0)&(ps_df['值']<50)] #异常值处理
    pe_df = pd.read_sql('select * from `pe`', con=conn)
    pe_df = pe_df[(pe_df['值'] > -100) & (pe_df['值'] < 200)]  # 异常值处理

    ror_df = pd.read_sql('select * from `ror`', con=conn)
    hror_df = pd.read_sql('select * from `hror`', con=conn)
    sec_ror_df = pd.read_sql('select * from `sec_ror`', con=conn).rename(columns={'index':'板块'})

    to_df = pd.read_sql('select * from `to`', con=conn)
    hto_df = pd.read_sql('select * from `hto`', con=conn)
    sec_to_df = pd.read_sql('select * from `sec_to`', con=conn).rename(columns={'index':'板块'})

    north1_df = pd.read_sql('select * from `north1`', con=conn)
    north2_df = pd.read_sql('select * from `north2`', con=conn)

    long_df = pd.read_sql('select * from `long`', con=conn)
    short_df = pd.read_sql('select * from `short`', con=conn)
    longshort_df = pd.read_sql('select * from `longshort`', con=conn)

    news_df = pd.read_sql('select * from `news`', con=conn)

    data_dic = {
        'ror_df':ror_df,
        'to_df':to_df,
        'hto_df':hto_df,
        'sec_to_df':sec_to_df,
        'close_df':close_df,
        'ps_df':ps_df,
        'pe_df':pe_df,
        'sec_ror_df':sec_ror_df,
        'hror_df':hror_df,
        'north1_df':north1_df,
        'north2_df':north2_df,
        'long_df':long_df,
        'short_df':short_df,
        'longshort_df':longshort_df,
        'news_df':news_df,
    }

    return data_dic

## 全局数据
Data_dic = getData()

## ===== 日涨跌幅 =====
## A股个股
ror_df = Data_dic['ror_df']
ror_df = ror_df[['股票名称', '申万行业分类', '值', '分位数']].rename(columns={'值':'日涨跌幅','分位数':'日涨跌幅-分位数'})

ror_df['行业'] = ror_df['申万行业分类'].apply(lambda x: x.split('--')[1])
fig1 = px.scatter(ror_df,  # 数据集
                    x="日涨跌幅",  # x轴
                    y="日涨跌幅-分位数",  # y轴
                    color='行业',
                    hover_data=['股票名称', "日涨跌幅","日涨跌幅-分位数",'行业',])
fig1.update_layout(yaxis_range=[0,1])

## A股板块
sec_ror_df = Data_dic['sec_ror_df']
sec_ror_df = sec_ror_df[['板块', '行业级别', '值', '分位数']].rename(columns={'值':'日涨跌幅','分位数':'日涨跌幅-分位数'})
sec_ror_df['size'] = 3
fig2 = px.scatter(sec_ror_df,  # 数据集
                    x="日涨跌幅",  # x轴
                    y="日涨跌幅-分位数",  # y轴
                    color='行业级别',
                    size='size',
                    hover_data=['板块', '日涨跌幅','日涨跌幅-分位数']
                  )
fig2.update_layout(yaxis_range=[0,1])

## 港股个股
hror_df = Data_dic['hror_df']
hror_df = hror_df[['股票名称', '值', '分位数']].rename(columns={'值':'日涨跌幅','分位数':'日涨跌幅-分位数'})

fig3 = px.scatter(hror_df,  # 数据集
                    x="日涨跌幅",  # x轴
                    y="日涨跌幅-分位数",  # y轴
                    hover_data=['股票名称', "日涨跌幅","日涨跌幅-分位数",])
fig3.update_layout(yaxis_range=[0,1])

## ===== 换手率 =====
## A股个股
to_df = Data_dic['to_df']
to_df = to_df[['股票名称', '申万行业分类', '值', '分位数']].rename(columns={'值':'换手率','分位数':'换手率-分位数'})

to_df['行业'] = to_df['申万行业分类'].apply(lambda x: x.split('--')[1])
fig4 = px.scatter(to_df,  # 数据集
                    x="换手率",  # x轴
                    y="换手率-分位数",  # y轴
                    color='行业',
                    hover_data=['股票名称', "换手率","换手率-分位数",'行业',])
fig4.update_layout(yaxis_range=[0,1])

## A股板块
sec_to_df = Data_dic['sec_to_df']
sec_to_df = sec_to_df[['板块', '行业级别', '值', '分位数']].rename(columns={'值':'换手率','分位数':'换手率-分位数'})
sec_to_df['size'] = 3
fig5 = px.scatter(sec_to_df,  # 数据集
                    x="换手率",  # x轴
                    y="换手率-分位数",  # y轴
                    color='行业级别',
                    size='size',
                    hover_data=['板块', '换手率','换手率-分位数']
                  )
fig5.update_layout(yaxis_range=[0,1])

## 港股个股
hto_df = Data_dic['hto_df']
hto_df = hto_df[['股票名称', '值', '分位数']].rename(columns={'值':'换手率','分位数':'换手率-分位数'})

fig6 = px.scatter(hto_df,  # 数据集
                    x="换手率",  # x轴
                    y="换手率-分位数",  # y轴
                    hover_data=['股票名称', "换手率","换手率-分位数",])
fig6.update_layout(yaxis_range=[0,1])

## ===== 北向资金 =====
## 持仓分布
north1_df = Data_dic['north1_df']
latest_date = north1_df['更新日'].max()
north1_df = north1_df[north1_df['更新日']==latest_date]
north1_sr = north1_df.groupby(by='三级行业')['值'].sum()

fig7 = px.pie(north1_sr.to_frame('持仓市值'),
              values='持仓市值',
              names=north1_sr.index)

## 持股变化
north2_df = Data_dic['north2_df']
latest_date = north2_df['更新日'].max()
north2_df = north2_df[north2_df['更新日']==latest_date]
north2_sr = north2_df.groupby(by='三级行业')['值'].sum() / 10000
north2_sr = north2_sr.sort_values(ascending=False)

fig8 = px.bar(north2_sr.to_frame('持股变化(万股)'),
              y='持股变化(万股)',
              x=north2_sr.index)

## ===== 融资融券 =====
## 融资余额
long_df = Data_dic['long_df']
latest_date = long_df['更新日'].max()
long_df = long_df[long_df['更新日']==latest_date]
long_df['行业'] = long_df['申万行业分类'].apply(lambda x: x.split('--')[1])
long_df = long_df[['股票名称', '值', '分位数', '行业']].rename(columns={'值':'融资余额','分位数':'融资余额-分位数'})

fig9 = px.scatter(long_df,  # 数据集
                    x="融资余额",  # x轴
                    y="融资余额-分位数",  # y轴
                    hover_data=['股票名称', "融资余额","融资余额-分位数",],
                    color='行业')

fig9.update_layout(yaxis_range=[0,1])

## 融券余额
short_df = Data_dic['short_df']
latest_date = short_df['更新日'].max()
short_df = short_df[short_df['更新日']==latest_date]
short_df['行业'] = short_df['申万行业分类'].apply(lambda x: x.split('--')[1])
short_df = short_df[['股票名称', '值', '分位数', '行业']].rename(columns={'值':'融券余额','分位数':'融券余额-分位数'})

fig10 = px.scatter(short_df,  # 数据集
                    x="融券余额",  # x轴
                    y="融券余额-分位数",  # y轴
                    hover_data=['股票名称', "融券余额","融券余额-分位数",],
                    color='行业')
fig10.update_layout(yaxis_range=[0,1])

## 融资余额-融券余额
longshort_df = Data_dic['longshort_df']
latest_date = longshort_df['更新日'].max()
longshort_df = longshort_df[longshort_df['更新日']==latest_date]
longshort_df['行业'] = longshort_df['申万行业分类'].apply(lambda x: x.split('--')[1])
longshort_df = longshort_df[['股票名称', '值', '分位数', '行业']].rename(columns={'值':'融资-融券余额','分位数':'融资-融券余额-分位数'})

fig11 = px.scatter(longshort_df,  # 数据集
                    x="融资-融券余额",  # x轴
                    y="融资-融券余额-分位数",  # y轴
                    hover_data=['股票名称', "融资-融券余额","融资-融券余额-分位数",],
                    color='行业')
fig11.update_layout(yaxis_range=[0,1])

## ===== 提醒内容生成 =====
def funcContent(name, data_df, high, low, multiple=1):

    df = data_df.copy().sort_values(by=f'{name}', ascending=False)
    ror_high_lt = df.iloc[:3, :]['股票名称'].tolist()
    ror_low_lt = df.iloc[-3:, :]['股票名称'].tolist()
    ib_high = df[f'{name}-分位数'] >= high
    if ib_high.sum() != 0: ror_high_lt += df[ib_high]['股票名称'].tolist()
    ib_low = df[f'{name}-分位数'] <= low
    if ib_low.sum() != 0: ror_low_lt += df[ib_low]['股票名称'].tolist()
    df2 = df.set_index('股票名称')

    ror_high_lt = list(set(ror_high_lt))
    ror_low_lt = list(set(ror_low_lt))

    str_h = ''
    for h in ror_high_lt:
        v_h = df2.at[h, f'{name}']/multiple
        str_h += f'{h}({v_h:.1%}),'

    str_l = ''
    for l in ror_low_lt:
        v_l = df2.at[l, f'{name}']/multiple
        str_l += f'{l}({v_l:.1%}),'

    return str_h[:-1], str_l[:-1]

def funcContent_sec(name, data_df, high, low, multiple=1):

    df = data_df.copy().sort_values(by=f'{name}', ascending=False).set_index('板块')
    ror_high_lt = list(df.iloc[:3, :].index)
    ror_low_lt = list(df.iloc[-3:, :].index)
    ib_high = df[f'{name}-分位数'] >= high
    if ib_high.sum() != 0: ror_high_lt += list(df[ib_high].index)
    ib_low = df[f'{name}-分位数'] <= low
    if ib_low.sum() != 0: ror_low_lt += list(df[ib_low].index)

    ror_high_lt = list(set(ror_high_lt))
    ror_low_lt = list(set(ror_low_lt))

    str_h = ''
    for h in ror_high_lt:
        v_h = df.at[h, f'{name}']/multiple
        str_h += f'{h}({v_h:.1%}),'

    str_l = ''
    for l in ror_low_lt:
        v_l = df.at[l, f'{name}']/multiple
        str_l += f'{l}({v_l:.1%}),'

    return str_h[:-1], str_l[:-1]

def funcContent_north(sr):

    sr_h = sr.head(3)
    str_h = ''
    for i in range(3):
        str_h += f'{sr_h.index[i]}({int(sr_h.iat[i])}),'

    sr_l = sr.tail(3)
    str_l = ''
    for i in range(2,-1,-1):
        str_l += f'{sr_l.index[i]}({int(sr_l.iat[i])}),'

    return str_h[:-1], str_l[:-1]

def funcContent_longshort(name, data_df, high, low, multiple=1):

    df = data_df.copy().sort_values(by=f'{name}', ascending=False)
    ror_high_lt = df.iloc[:3, :]['股票名称'].tolist()
    ror_low_lt = df.iloc[-3:, :]['股票名称'].tolist()
    ib_high = df[f'{name}-分位数'] >= high
    if ib_high.sum() != 0: ror_high_lt += df[ib_high]['股票名称'].tolist()
    ib_low = df[f'{name}-分位数'] <= low
    if ib_low.sum() != 0: ror_low_lt += df[ib_low]['股票名称'].tolist()
    df2 = df.set_index('股票名称')

    ror_high_lt = list(set(ror_high_lt))
    ror_low_lt = list(set(ror_low_lt))

    str_h = ''
    for h in ror_high_lt:
        v_h = df2.at[h, f'{name}']/multiple
        str_h += f'{h}({v_h:.1f}),'

    str_l = ''
    for l in ror_low_lt:
        v_l = df2.at[l, f'{name}']/multiple
        str_l += f'{l}({v_l:.1f}),'

    return str_h[:-1], str_l[:-1]


def getContent():

    high = 0.99
    low = 0.01
    # 日涨跌幅
    str_ror_high, str_ror_low = funcContent('日涨跌幅', ror_df, high, low)
    str_sec_ror_high, str_sec_ror_low = funcContent_sec('日涨跌幅', sec_ror_df, high, low)
    str_hror_high, str_hror_low = funcContent('日涨跌幅', hror_df, high, low)
    # 换手率
    str_to_high, str_to_low = funcContent('换手率', to_df, 0.995, 0.005, multiple=100)
    str_sec_to_high, str_sec_to_low = funcContent_sec('换手率', sec_to_df, 0.995, 0.005, multiple=100)
    str_hto_high, str_hto_low = funcContent('换手率', hto_df, 0.995, 0.005, multiple=100)
    # 北向资金
    str_north_high, str_north_low = funcContent_north(north2_sr)
    # 融资-融券余额
    str_longshort_high, str_longshort_low = funcContent_longshort('融资-融券余额', longshort_df, 0.995, 0.005, multiple=100000000)

    daily_content = f'''
    **【日涨跌幅】**\n
    **A股个股**\r
    ~~~
    涨：{str_ror_high}\r
    跌：{str_ror_low}
    ~~~
    **A股板块**\r
    ~~~
    涨：{str_sec_ror_high}\r
    跌：{str_sec_ror_low}
    ~~~
    **港股个股**\r
    ~~~
    涨：{str_hror_high}\r
    跌：{str_hror_low}
    ~~~
    **【换手率】**\n
    **A股个股**\r
    ~~~
    高：{str_to_high}\r
    低：{str_to_low}
    ~~~
    **A股板块**\r
    ~~~
    高：{str_sec_to_high}\r
    低：{str_sec_to_low}
    ~~~
    **港股个股**\r
    ~~~
    高：{str_hto_high}\r
    低：{str_hto_low}
    ~~~
    **【北向资金】**\n
    **持股变化(万股)**\r
    ~~~
    流入前3行业：{str_north_high}\r
    流入后3行业：{str_north_low}
    ~~~
    **【融资融券】**\n
    **融资-融券余额(亿元)**\r
    ~~~
    高：{str_longshort_high}\r
    低：{str_longshort_low}
    ~~~
    '''

    daily_content_download = f'''
        【日涨跌幅】\r
        >>> A股个股 <<<\r
        涨：{str_ror_high}\r
        跌：{str_ror_low}
        >>> A股板块 <<<\r
        涨：{str_sec_ror_high}\r
        跌：{str_sec_ror_low}
        >>> 港股个股 <<<\r
        涨：{str_hror_high}\r
        跌：{str_hror_low}
        【换手率】\r
        >>> A股个股 <<<\r
        高：{str_to_high}\r
        低：{str_to_low}
        >>> A股板块 <<<\r
        高：{str_sec_to_high}\r
        低：{str_sec_to_low}
        >>> 港股个股 <<<\r
        高：{str_hto_high}\r
        低：{str_hto_low}
        【北向资金】\r
        >>> 持股变化(万股) <<<\r
        流入前3行业：{str_north_high}\r
        流入后3行业：{str_north_low}
        【融资融券】\r
        >>> 融资-融券余额(亿元) <<<\r
        高：{str_longshort_high}\r
        低：{str_longshort_low}
        
        ————————————————————
        具体可参看网页：https://share.streamlit.io/xiaoxiangtear/daily-monitor/main/daily_app.py
        
        '''

    return daily_content, daily_content_download

## Streamlit可视化
## >>>>> 页面主体 <<<<<
ror_df2 = Data_dic['ror_df']
latest_date = ror_df2['更新日'].max()
st.title(f'每日监测（更新日期：{latest_date}）')
content, content_download = getContent()
st.write(content)
st.download_button('下载', content_download, f'每日监测（更新日期：{latest_date}）.txt')

st.markdown('## 日涨跌幅')
col1, col2, col3= st.columns(3)
col1.markdown('### A股个股')
col1.plotly_chart(fig1, use_container_width=True)
col2.markdown('### A股板块')
col2.plotly_chart(fig2, use_container_width=True)
col3.markdown('### 港股个股')
col3.plotly_chart(fig3, use_container_width=True)

st.markdown('## 换手率')
col1, col2, col3= st.columns(3)
col1.markdown('### A股个股')
col1.plotly_chart(fig4, use_container_width=True)
col2.markdown('### A股板块')
col2.plotly_chart(fig5, use_container_width=True)
col3.markdown('### 港股个股')
col3.plotly_chart(fig6, use_container_width=True)

st.markdown('## 北向资金')
col1, col2, col3= st.columns(3)
col1.markdown('### 行业持仓分布')
col1.plotly_chart(fig7, use_container_width=True)
col2.markdown('### 行业持股变化')
col2.plotly_chart(fig8, use_container_width=True)

st.markdown('## 融资融券')
col1, col2, col3= st.columns(3)
col1.markdown('### 融资余额')
col1.plotly_chart(fig9, use_container_width=True)
col2.markdown('### 融券余额')
col2.plotly_chart(fig10, use_container_width=True)
col3.markdown('### 融资-融券余额')
col3.plotly_chart(fig11, use_container_width=True)

# st.markdown('## 医药生物行业相关新闻') 没有wnd权限了
# news_df = Data_dic['news_df'][['time', 'title', 'url', 'source', 'relevant_windcodes']]
# st.dataframe(news_df)
# st.table(news_df)


## >>>>> css设置 <<<<<
hide_menu_style = """
        <style>
            #MainMenu {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)
