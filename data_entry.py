import PySimpleGUI as sg
from datetime import datetime
import pandas as pd
import sys
import os

# Resource path function:
# Source code: https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Add color to window
sg.theme('DarkBlue13')

EXCEL_FILE = os.path.abspath('C:/Users/yuvem/Baby Schedule/Data_Entry.xlsx')

df = pd.read_excel(EXCEL_FILE)

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Name', size=(15,1)), sg.InputText(key='Name')],
    [sg.Input(key='Date', size=(20,1)), 
     sg.CalendarButton("Datetime", close_when_date_chosen=True, target="Date", location=(1000, 640), no_titlebar=False)],
    [sg.Text('What are you recording?', size=(30,1)), sg.Combo(['Sleep','Feeding','Diaper'], key='What are you recording?')],
    #[sg.Text('Date', size=(15,1)), sg.InputText(key='Date')],
    #[sg.Text('Time', size=(15,1)), sg.InputText(key='Time')],
    #[sg.Text('Which are you recording for?: "Sleep, Feeding, Diapers"', size=(40,1)), sg.InputText(key='RecordingType')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
]

# Initialize window
window = sg.Window('Baby schedule entry form', layout)

# Clear function
def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        new_data = pd.DataFrame([values])  # Create a DataFrame with the new data
        df = pd.concat([df, new_data], ignore_index=True)  # Concatenate the DataFrames
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Saved!')
        clear_input()
        #print(event, values)
window.close()