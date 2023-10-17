import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,messagebox

path = None
save_as_dir = None

def sale_report(path,save_as):
    import pandas as pd
    import os
    import datetime

    today = datetime.date.today()
    year = today.year-1


    xlsx_file_lists = []
  
    for root,dirs,files in os.walk(path):
        for name in files:
            file_path = os.path.join(root,name)
            xlsx_file_lists.append(file_path)

    df_lists = []
    for f in xlsx_file_lists:
        if f.split("\\")[-2] == str(year):
            df = pd.read_excel(f)
            df_lists.append(df) #making list of df

    df_sumary = pd.concat(df_lists)
    df_sumary

    pivot = pd.pivot_table(df_sumary,
        index="transaction_date",
        columns="store",
        values="amount",
        aggfunc="sum")

    summary_monthly = pivot.resample("M").sum()
    summary_monthly

    import matplotlib
    fig = summary_monthly.plot(kind="bar",figsize=(20,12),fontsize=26,title="Monthly sale summary").get_figure()

    import xlwings as xw

    import datetime
    now = datetime.datetime.now()
    date_file_name = f'{str(now.date())}_{str(now.time()).split(".")[0].replace(":","_")}'


    template = xw.Book(r"data\sale_template.xlsx")

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

    template.save(f"{save_as}.xlsx")
    template.close()
    app.kill()


def browse_files():
    global path

    file_name = filedialog.askdirectory()
    path = file_name
    file_explorer_label.configure(text=path)


def save_as():
    global save_as_dir
    save_file = filedialog.asksaveasfilename(initialdir = "/",
                                          title = "save as a File",
                                          filetypes = (("excel files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))
    save_as_dir = save_file
    save_as_label.configure(text=save_as_dir)

def create_report_button_clicked():
    try:
        global path,save_as_dir
        print(f'path: {path}, save: {save_as_dir}')
        sale_report(path,save_as_dir)
        file_explorer_label.config(text="browse files")
        save_as_label.config(text="Save as")
        messagebox.showinfo("info","Done")
    except Exception as e:
        messagebox.showerror("Error!!",e)
        # print("Error",e)


#setup frame
window = tk.Tk()
window.title("Sale repot program")
window.geometry("640x120")
window.resizable(False,False)
frame = ttk.Frame(window)

#option
options = {'padx':5, 'pady':5}

#label browse_files
file_explorer_label = ttk.Label(frame, text="Browse files", width=85)
file_explorer_label.grid(column=0,row=0,**options)


#button browse_files
browse_files_btn = ttk.Button(frame,text='Browse')
browse_files_btn.grid(column=1,row=0,**options)
browse_files_btn.configure(command=browse_files)

#label save_as
save_as_label = ttk.Label(frame, text="Save as",width=85)
save_as_label.grid(column=0,row=1,**options)


#button save_as
save_as_button = ttk.Button(frame,text='File location')
save_as_button.grid(column=1,row=1,**options)
save_as_button.configure(command=save_as)


#button Create
create_button = ttk.Button(frame,text='CREATE!')
create_button.grid(columnspan=2,row=3,**options)
create_button.configure(command=create_report_button_clicked)


# add grid
frame.grid(pady=10,padx=10)

#loop gui
window.mainloop()