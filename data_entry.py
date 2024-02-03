import PySimpleGUI as sg
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
EXCEL_FILE_TWO = os.path.abspath('C:/Users/yuvem/Baby Schedule/Data_Entry2.xlsx')

df = pd.read_excel(EXCEL_FILE)
df_2 = pd.read_excel(EXCEL_FILE_TWO)

# Define color for the "Submit" button
submit_button_color = ('white', '#43A173')

# Define image for table
image_vital_signs = 'C:/Users/yuvem/Baby Schedule/vital_signs_img.png'

instructions_layout = [
    [sg.Text("In the 'Baby Schedule' tab, enter your name, datetime, choose what you're recording (Sleep, Feeding, or Diaper), \nand any comments. In the 'Baby Vitals' tab, enter your name, datetime, choose what you're recording \n(Temperature, Heart Rate, BP, Respiration, Weight, Height). \n \nBelow is a guide for pediatric vital sign normal ranges.", text_color='black', background_color="#CBD9F4")],
    [sg.Image(filename=image_vital_signs)]
]

sleep_feed_diaper_layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Name', size=(15, 1)), sg.InputText(key='Name')],
    [sg.Input(key='Date', size=(20, 1)),
     sg.CalendarButton("Datetime", close_when_date_chosen=True, target="Date", location=(1000, 640), no_titlebar=False, key='Datetime')],
    [sg.Text('What are you recording?', size=(30, 1)), sg.Combo(['Sleep', 'Feeding', 'Diaper'], key='What are you recording?')],
    [sg.Submit(size=(8,1), button_color=submit_button_color)]
]

baby_vitals_layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Name', size=(15, 1)), sg.InputText(key='Name2')],
    [sg.Input(key='Date2', size=(20, 1)),
     sg.CalendarButton("Datetime", close_when_date_chosen=True, target="Date2", location=(1000, 640), no_titlebar=False, key='Datetime2')],
    [sg.Text('Which are you recording?', size=(30, 1)), sg.Combo(['Temperature', 'Heart Rate', 'BP', 'Respiration', 'Weight', 'Height'], key='Which are you recording?')],
    [sg.Text('Value', size=(15, 1)), sg.InputText(key='Value')],    
    [sg.Button("Enter", size=(8,1), button_color="#43A173")]
]

# Tab Group
tab_group = [
    [sg.TabGroup(
        [[
        sg.Tab('Instructions', instructions_layout, background_color="#CBD9F4"),
        sg.Tab('Baby Schedule', sleep_feed_diaper_layout),
        sg.Tab('Baby Vitals', baby_vitals_layout)]],
        tab_location='centertop',
        border_width=5),
        sg.Button('Clear', button_color="#CB5757"),
        sg.Exit()
    ]]

# Initialize window
window = sg.Window('Baby Schedule Entry Form', tab_group)

# Clear function
def clear_input(values):
    for key in values:
        window[key]('')
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Clear':
        clear_input(values)
    elif event == 'Submit':
        new_data = pd.DataFrame([values])  # Create a DataFrame with the new data
        df = pd.concat([df, new_data], ignore_index=True)  # Concatenate the DataFrames
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Saved!')
        clear_input(values)
        window['Datetime'].update(visible=True)
        
    elif event == "Enter":
        new_data_2 = pd.DataFrame([values])  # Create a DataFrame with the new data
        df_2 = pd.concat([df_2, new_data_2], ignore_index=True)  # Concatenate the DataFrames
        df_2.to_excel(EXCEL_FILE_TWO, index=False)
        sg.popup('Saved!')
        clear_input(values)
        window['Datetime'].update(visible=True)

window.close()
