# %% [markdown]
# # Tkinter

# %%
# !pip install tk

# %%
import tkinter as tk
from tkinter import ttk

def fahrenheit_to_celsius(f):
    """convert fahrenhite to celsius"""
    result = round((f - 32) * 5/9,2)
    return result

def convert_button_clicked():
    """get temperature from entry then convert it"""
    f = float(temperature.get())
    c = fahrenheit_to_celsius(f)
    result_label.config(text=c) #change value of result_label 


#setup frame
window = tk.Tk()
window.title("Temperature Convert")
window.geometry("300x70")
window.resizable(False,False)
frame = ttk.Frame(window)

#option
options = {'padx':5, 'pady':5}

#label
temperature_label = ttk.Label(frame, text="Fahrenheit")
temperature_label.grid(column=0,row=0,**options)

#input box
temperature = tk.StringVar()
temperature_input = ttk.Entry(frame,textvariable=temperature)
temperature_input.grid(column=1,row=0,**options)

#button
convert_button = ttk.Button(frame,text='Convert')
convert_button.grid(column=2,row=0,**options)
convert_button.configure(command=convert_button_clicked)


#result label
result_label = ttk.Label(frame, text="Input temperature")
result_label.grid(columnspan=2,row=1,**options)

# add grid
frame.grid(pady=12,padx=7)

#loop gui
window.mainloop()


# !pip install pyinstaller


