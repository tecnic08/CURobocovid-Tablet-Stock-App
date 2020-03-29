#!/usr/bin/env python3

import tkinter as tk
import csv
import time
from csv import writer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
    6: 'Location'
}

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

        ## Seach Area
        # Labels
        tk.Label(self, text="Search and Update").grid(row=0, columnspan=2, sticky="ew")
        tk.Label(self, text="Search:").grid(row=1, sticky="e")
        
        # Entry
        self.search_string = tk.StringVar()
        self.search_field = tk.Entry(self, textvariable=self.search_string, width=20)
        self.search_field.grid(row=1, column=1, sticky="we")

        # Search Button
        search = tk.Button(self, text="Search", width = 10, command=self.search)
        search.grid(row=2, column=1, sticky="w")

        # Label
        tk.Label(self, text="IMEI:").grid(row=4,sticky="e")
        tk.Label(self, text="Serial Number:").grid(row=5,sticky="e")
        tk.Label(self, text="Phone Number:").grid(row=6, sticky="e")
        tk.Label(self, text="ICCID:").grid(row=7, sticky="e")
        tk.Label(self, text="Deployed Location:").grid(row=8, sticky="e")

        # Entries
        self.imei_string = tk.StringVar()
        self.serialNumber_string = tk.StringVar()
        self.phoneNumber_string = tk.StringVar()
        self.iccid_string = tk.StringVar()
        self.location_string = tk.StringVar()

        # Entries Field
        self.imei = tk.Entry(self, textvariable=self.imei_string, width=20, state=tk.DISABLED)
        self.serialNo = tk.Entry(self, textvariable=self.serialNumber_string, width=20)
        self.phoneNo = tk.Entry(self, textvariable=self.phoneNumber_string, width=20)
        self.iccid = tk.Entry(self, textvariable=self.iccid_string, width=20)
        self.location = tk.Entry(self, textvariable=self.location_string, width=20)

        # Field Properties
        self.imei.grid(row=4, column=1, sticky="we")
        self.serialNo.grid(row=5, column=1, sticky="we")
        self.phoneNo.grid(row=6, column=1, sticky="we")
        self.iccid.grid(row=7, column=1, sticky="we")
        self.location.grid(row=8, column=1, sticky="we")

        # Update Button
        self.updateButton = tk.Button(self, text="Update", width = 10, command=self.update, state=tk.DISABLED)
        self.updateButton.grid(row=9, column=1, sticky="w")

        # Cancel Button
        self.cancelButton = tk.Button(self, text="Cancel", width = 5, command=self.clearEntries)
        self.cancelButton.grid(row=9, column=0, sticky="e")

        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready to seach...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=50, state='disabled')
        self.status.grid(row=10,column=0, columnspan=2, sticky="ws")

        # Binding
        self.search_field.bind("<Return>", self.search)

        self.imei.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.serialNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.phoneNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.iccid.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.location.bind("<Return>", self.update)

        # Focus to search box
        self.search_field.focus()

    def clearEntries(self, event=None, clear_search_field=True):
        self.imei_string.set('')
        self.serialNo.delete(0, 'end')
        self.phoneNo.delete(0, 'end')
        self.location.delete(0, 'end')
        self.iccid.delete(0,'end')
        self.serialNo.focus()

        if (clear_search_field):
            self.search_field.delete(0, 'end')
            self.search_field.focus()
        
        self.updateButton['state'] = tk.DISABLED
        

    def search(self, event=None):
        try:
            # Clear current result
            self.clearEntries(clear_search_field = False)

            # Do not allow empty search
            if (len(self.search_string.get()) < 5):
                self.statusText.set("Search string too short!")
                return

            self.statusText.set("Searching...")
            self.target_search_loc = worksheet.find(self.search_string.get())

            # Do not allow search with location or time
            if (column_definition[self.target_search_loc.col] == 'Location' or column_definition[self.target_search_loc.col] == 'Updated Time'):
                self.statusText.set("Cannot search with location or time!")
                return

            self.statusText.set("Found " + self.search_string.get() + " as " + column_definition[self.target_search_loc.col] + ".")

            # get the whole row
            row = worksheet.row_values(self.target_search_loc.row, value_render_option='UNFORMATTED_VALUE')
            
            # enable update button
            self.updateButton['state'] = tk.NORMAL

            # update each field
            self.imei_string.set(row[1])
            self.serialNumber_string.set(row[2])
            self.phoneNumber_string.set(row[3])
            self.iccid_string.set(row[4])
            self.location_string.set(row[5])

         # there are some cells that is empty, this is normal
        except IndexError:
            return

        # not found
        except gspread.exceptions.CellNotFound:
            self.statusText.set(self.search_string.get() + " NOT found.")
            self.search_field.focus()
            return
    
    def update(self, event=None):

        try:
            # update each item in a row
            worksheet.update_cell(self.target_search_loc.row, 1, time.time()) #time
            worksheet.update_cell(self.target_search_loc.row, 2, self.imei_string.get()) #imei
            worksheet.update_cell(self.target_search_loc.row, 3, self.serialNumber_string.get()) #serialNumber
            worksheet.update_cell(self.target_search_loc.row, 4, self.phoneNumber_string.get()) #phoneNumber
            worksheet.update_cell(self.target_search_loc.row, 5, self.iccid_string.get()) #iccid
            worksheet.update_cell(self.target_search_loc.row, 6, self.location_string.get()) #location
            
            self.target_search_loc = None
            self.statusText.set("Updated " + self.imei_string.get())
            self.clearEntries()

        except AttributeError:
             self.statusText.set("Search First!")
             return



# GUI settings
root = tk.Tk()
app = App(root)
root.title("COVID-19 Tablet Data Update")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()