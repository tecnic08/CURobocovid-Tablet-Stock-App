#!/usr/bin/env python3

import tkinter as tk
import csv
import time
from csv import writer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from print import *
from config import *

print("Connecting to Google Drive API...")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(clientCredentialFile, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open(useDatabase)

# Extract and print all of the values
worksheet = sheet.get_worksheet(0)

print("Connected to " + useDatabase)

column_definition = {
    1: 'Updated Time',
    2: 'IMEI',
    3: 'Serial Number',
    4: 'Phone Number',
    5: 'ICCID',
    6: 'Location',
    7: 'Sub Location',
    8: 'Project',
    9: 'Mode',
    10: 'Cellular Operator'
}

deviceModeOptions = [
    'Patient',
    'Doctor',
    'Development'
]

projectOptions = [
    'Telepresence',
    'Pinto',
    'Development'
]

def popup(title, msg):
    '''Open popup window with title and msg'''
    w = tk.Toplevel(root)
    w.title(title)
    w.minsize(200, 200)
    tk.Label(w, text=msg).pack()
    tk.Button(w, text="Close", command=w.destroy).pack(pady=10)
    w.bind("<Return>", lambda f: w.destroy())

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(anchor="w")


        tk.Label(self, text="Location Assignment").grid(row=0, columnspan=2, sticky="ew")

        ## Seach Area
        # Labels
        tk.Label(self, text="Identifier:").grid(row=1, sticky="e")
        self.search_string = tk.StringVar()
        self.search_field = tk.Entry(self, textvariable=self.search_string, width=40)
        self.search_field.grid(row=1, column=1, sticky="we")

        ## Location Input Area
        tk.Label(self, text="Location").grid(row=2, columnspan=2, sticky="we")
        # Labels
        tk.Label(self, text="Target Location:").grid(row=3, sticky="e")
        self.target_location_string = tk.StringVar()
        self.target_location_field = tk.Entry(self, textvariable=self.target_location_string, width=40)
        self.target_location_field.grid(row=3, column=1, sticky="we")

        tk.Label(self, text="Sub Location:").grid(row=4, sticky="e")
        self.target_sub_location_string = tk.StringVar()
        self.target_sub_location_field = tk.Entry(self, textvariable=self.target_sub_location_string, width=40)
        self.target_sub_location_field.grid(row=4, column=1, sticky="we")
        
        tk.Label(self, text="Project:").grid(row=5, sticky="e")
        self.target_project_string = tk.StringVar()
        self.target_project_string.set(projectOptions[0])
        self.target_project_field = tk.OptionMenu(self, self.target_project_string, *projectOptions)
        self.target_project_field.grid(row=5, column=1, sticky="we")

        tk.Label(self, text="Device Mode:").grid(row=6, sticky="e")
        self.target_device_mode_string = tk.StringVar()
        self.target_device_mode_string.set(deviceModeOptions[0])
        self.target_device_mode_field = tk.OptionMenu(self, self.target_device_mode_string, *deviceModeOptions)
        self.target_device_mode_field.grid(row=6, column=1, sticky="we")

        # Assign Button
        assignButton = tk.Button(self, text="Assign", width = 10, command=self.searchAndUpdate)
        assignButton.grid(row=7, column=1, sticky="w")

        # Print Checkbox
        self.printCheck = tk.IntVar()
        self.printCheck.set(1)
        checkButton = tk.Checkbutton(self, text="Print Label", variable=self.printCheck)
        checkButton.grid(row=7, column = 1, sticky="e")


        ## Records
        tk.Label(self, text="Current Records").grid(row=8, columnspan=2,sticky="we")
        # Label
        tk.Label(self, text="IMEI:").grid(row=9,sticky="e")
        self.imei_string = tk.StringVar()
        self.imei = tk.Entry(self, textvariable=self.imei_string, width=40, state=tk.DISABLED)
        self.imei.grid(row=9, column=1, sticky="we")

        tk.Label(self, text="Serial Number:").grid(row=10,sticky="e")
        self.serialNumber_string = tk.StringVar()
        self.serialNo = tk.Entry(self, textvariable=self.serialNumber_string, width=40, state=tk.DISABLED)
        self.serialNo.grid(row=10, column=1, sticky="we")
        
        tk.Label(self, text="Cellular Information:").grid(row=11, sticky="e")
        self.cellularInfo_string = tk.StringVar()
        self.cellularInfo = tk.Entry(self, textvariable=self.cellularInfo_string, width=40, state=tk.DISABLED)
        self.cellularInfo.grid(row=11, column=1, sticky="we")
        
        tk.Label(self, text="Deployed Location:").grid(row=12, sticky="e")
        self.location_string = tk.StringVar()
        self.location = tk.Entry(self, textvariable=self.location_string, width=40, state=tk.DISABLED)
        self.location.grid(row=12, column=1, sticky="we")

        tk.Label(self, text="Device Mode:").grid(row=13, sticky="e")
        self.deviceMode_string = tk.StringVar()
        self.deviceMode = tk.Entry(self, textvariable=self.deviceMode_string, width=40, state=tk.DISABLED)
        self.deviceMode.grid(row=13, column=1, sticky="we")

        # Clear All Button
        self.cancelButton = tk.Button(self, text="Clear All", width = 5, command=self.clearEntries)
        self.cancelButton.grid(row=14, column=1, sticky="e")

        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready to seach...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=70, state='disabled')
        self.status.grid(row=15,column=0, columnspan=2, sticky="ws")

        # Binding
        self.target_location_field.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.search_field.bind("<Return>", self.searchAndUpdate)

        # Focus to search box
        self.search_field.focus()

    def clearEntries(self, event=None, clear_target_location_field=True):
        self.imei_string.set('')
        self.serialNumber_string.set('')
        self.cellularInfo_string.set('')
        self.deviceMode_string.set('')
        self.location_string.set('')

        if (clear_target_location_field):
            self.search_field.delete(0,'end')
            self.target_location_field.delete(0,'end')
            self.target_sub_location_field.delete(0,'end')
            self.search_field.focus()
        

    def searchAndUpdate(self, event=None):
        try:
            # Clear current result
            self.clearEntries(clear_target_location_field = False)

            # Do not allow empty search
            if (len(self.search_string.get()) < 5):
                self.statusText.set("Search string too short!")
                return

            self.statusText.set("Searching...")
            self.target_search_loc = worksheet.find(self.search_string.get())

            # Only allow search with IMEI / SN / Phone Number / ICCID
            if (self.target_search_loc.col < 2 or self.target_search_loc.col > 5):
                self.statusText.set("Only accept IMEI / SN / Phone Number / ICCID")
                return

            self.statusText.set("Found " + self.search_string.get() + " as " + column_definition[self.target_search_loc.col] + ".")

            # Update time and location
            worksheet.update_cell(self.target_search_loc.row, 1, time.time()) #time
            worksheet.update_cell(self.target_search_loc.row, 6, self.target_location_string.get()) #location
            worksheet.update_cell(self.target_search_loc.row, 7, self.target_sub_location_string.get()) #sub location
            worksheet.update_cell(self.target_search_loc.row, 8, self.target_project_string.get()) #project
            worksheet.update_cell(self.target_search_loc.row, 9, self.target_device_mode_string.get()) #mode
            
            # get the whole row
            row = worksheet.row_values(self.target_search_loc.row, value_render_option='UNFORMATTED_VALUE')

            # Clear search field
            self.search_field.delete(0, 'end')
            self.search_field.focus()

            # just for printing
            phoneNumber_str = row[3]
            iccid_str = row[4]

            # update each field for displaying
            self.imei_string.set(row[1])
            self.serialNumber_string.set(row[2])
            self.cellularInfo_string.set("0{} / {}".format(phoneNumber_str, row[9]))
            self.location_string.set("{} {}".format(row[5],row[6]))
            self.deviceMode_string.set("{} {}".format(row[7], row[8]))

            if (self.printCheck.get() == 1):
                generateAndPrint(self.imei_string.get(), self.serialNumber_string.get(), phoneNumber_str, iccid_str, self.location_string.get(),self.target_sub_location_string.get(), self.target_device_mode_string.get(), 1)

         # there are some cells that is empty, this is normal
        except IndexError:
            return

        # not found
        except gspread.exceptions.CellNotFound:
            self.statusText.set(self.search_string.get() + " NOT found.")
            self.search_field.focus()

# GUI settings
root = tk.Tk()
app = App(root)
root.title("COVID-19 Tablet Location Update")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()