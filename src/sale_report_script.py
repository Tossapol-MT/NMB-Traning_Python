# %% [markdown]
# # Excel sales report summary

import pandas as pd
import datetime
import os 

today = datetime.date.today()
year = today.year-1

path = r'D:\NMB-Traning_Python\src\data\sales_data'
xlsx_file_lists = []

today = datetime.date.today()
year = today.year-1

for root, dirs, files in os.walk(path):
    for name in files:
        file_path = os.path.join(root,name)
        if file_path.split("\\")[5] == str(year):
            xlsx_file_lists.append(file_path)
# print(xlsx_file_lists)

df_lists = []
for f in xlsx_file_lists:
    df = pd.read_excel(f)
    df_lists.append(df)
df_lists

df_summary = pd.concat(df_lists)
df_summary

pivot = pd.pivot_table(df_summary,index="transaction_date",columns="store",values="amount",aggfunc="sum")
pivot

summary_monthly = pivot.resample("M").sum()
summary_monthly


import matplotlib
fig = summary_monthly.plot(kind="bar",figsize=(20,12),fontsize="26",title="monthly sale summary").get_figure()


import xlwings as xw

now = datetime.datetime.now()
date_file_name = f'{str(now.date())}_{str(now.time()).split(".")[0].replace(":","_")}'

template = xw.Book(r"D:\NMB-Traning_Python\src\export\sale_template.xlsx")

app = xw.apps.active
sheet = template.sheets["summary"]
sheet["A1"].value = summary_monthly

pivot_page = template.sheets["pivot"]
pivot_page["A1"].value = pivot

#add picture
sheet_report = template.sheets["report"]
sheet_report["A1"].value = "Summary by month"
sheet_report['A1'].font.size = 24
sheet_report["A1"].api.Font.Bold = True
plot= sheet_report.pictures.add(fig,top=sheet["A3"].top,left=sheet["A3"].left)
plot.width = plot.width*0.8
plot.height = plot.height*0.8

template.save(f"export\script_summary_sale_report_{date_file_name}.xlsx")
template.close()
app.kill()


