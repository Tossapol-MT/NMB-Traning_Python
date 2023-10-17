# %% [markdown]
# # Excel sales report summary

# %%
import pandas as pd
import os
import datetime

today = datetime.date.today()
year = today.year-1


xlsx_file_lists = []
path =  r"D:\NMB-Traning_Python\src\data\sales_data"
for root,dirs,files in os.walk(path):
    for name in files:
        file_path = os.path.join(root,name)
        xlsx_file_lists.append(file_path)
        # print(xlsx_file_lists)

df_lists = []
for f in xlsx_file_lists:
    if f.split("\\")[-2] == str(year):
        df = pd.read_excel(f)
        df_lists.append(df) #making list of df
        
# df_lists

# %%
len(df_lists)

# %%
df_sumary = pd.concat(df_lists)
df_sumary

# %%
pivot = pd.pivot_table(df_sumary,
    index="transaction_date",
    columns="store",
    values="amount",
    aggfunc="sum")
# pivot

# %%
summary_monthly = pivot.resample("M").sum()
summary_monthly

# %%
import matplotlib
fig = summary_monthly.plot(kind="bar",figsize=(20,12),fontsize=26,title="Monthly sale summary").get_figure()

import xlwings as xw

import datetime
now = datetime.datetime.now()
date_file_name = f'{str(now.date())}_{str(now.time()).split(".")[0].replace(":","_")}'


template = xw.Book(r"D:\NMB-Traning_Python\src\data\sale_template.xlsx")

app = xw.apps.active
sheet = template.sheets["summary"]
sheet["A1"].value = summary_monthly

pivote = template.sheets["pivot"]
pivote["A1"].value = pivot

# add picture
sheet_report = template.sheets["report"]
sheet_report["A1"].value = "Summary by month"
sheet_report['A1'].font.size = 24
sheet_report["A1"].api.Font.Bold = True
plot= sheet_report.pictures.add(fig,top=sheet["A3"].top,left=sheet["A3"].left)
plot.width = plot.width*0.8
plot.height = plot.height*0.8

# template.save(f"D:/NMB-Traning_Python/src/export/summary_sale_report_{date_file_name}.xlsx")
template.save(f"D:\\NMB-Traning_Python/src/export/summary_sale_report_{date_file_name}.xlsx")
template.close()
app.kill()


