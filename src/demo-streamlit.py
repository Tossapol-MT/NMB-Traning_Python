import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="DATA analytics App",
    page_icon="🥺",
    layout="wide"
)

st.title("TITLE")
st.header("header")
st.subheader("subheader")
st.write("Hello World")
st.caption("Caption")

df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
st.dataframe(df,width=1500)

st.area_chart(df)
st.line_chart(df)
st.scatter_chart(df)


data = pd.DataFrame(data=np.random.rand(4,4)*100000,
index=["Q1","Q2","Q3","Q4"],
columns=["East","West","North","South"])
data.index.name = "Quaters"
data.columns.name = "Region"
fig = data.plot.bar().get_figure()
st.pyplot(fig)

import plotly.express as px

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


if st.button("Submit"):
    st.write("Click submit")

def converst_df(df):
    return df.to_csv().encode('utf-8')

csv = converst_df(df)

st.download_button(
    label="download data csv",
    data=csv,
    file_name='df.csv',
    mime='text/csv', 
)