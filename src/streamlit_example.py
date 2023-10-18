import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.set_page_config(
    page_title="DATA analytics App",
    page_icon="⛱️",
    layout="wide"
)

st.title("DEMO DATA ANALYTIC APP")

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

start_date = st.sidebar.date_input("Start date",today) # add sidebar
end_date = st.sidebar.date_input("End date",tomorrow)


report, upload_file = st.tabs(["REPORT","UPLOAD FILE"])

with report:
    df = pd.read_excel("./db/file.xlsx")
    df['stopDate'] = pd.to_datetime(df['StopTime'])  
    # mask = (df['stopDate'] > str(start_date)) & (df['stopDate'] <= str(end_date))
    mask = (df['stopDate'] >= str(start_date)) & (df['stopDate'] < str(end_date+datetime.timedelta(days=1)))
    df_process = df.loc[mask]
    # st.line_chart(df_process[["stopDate","Bland V bright"]])
    # df_plot = df_process[["stopDate","Bland V bright"]].reset_index()
    df_plot = df_process[["stopDate","Band V bright"]]

    fig, ax = plt.subplots()
    ax.plot(df_plot["stopDate"], df_plot["Band V bright"])
    st.pyplot(fig)

    # st.write(str(start_date))
    # st.dataframe(df['stopDate'])
    # st.dataframe(df_process)

    with st.expander("See data explanation"):
        st.dataframe(df_plot, width=700)
        st.download_button(
        "EXPORT CSV",
        df_plot.to_csv(index=False).encode('utf-8'),
        "file.csv",
        "text/csv")
          



with upload_file:
    with st.form("upload_file"):
                        uploaded_file = st.file_uploader("Choose a file")
                        if uploaded_file is not None:
                            df_upload_file = pd.read_excel(uploaded_file)
                            df_upload_file.to_excel("./db/file.xlsx")

                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            if uploaded_file is not None:
                                st.dataframe(df_upload_file,width=1000)
    
