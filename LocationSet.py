#!/usr/bin/env python3

import tkinter as tk
import csv
import time
from csv import writer
import gspread
from oauth2client.service_account import ServiceAccountCredentials

print("Connecting to Google Drive API...")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Tablet Database Dev")

# Extract and print all of the values
worksheet = sheet.get_worksheet(0)

print("Connected!!")

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


        tk.Label(self, text="Location Assignment").grid(row=0, columnspan=2, sticky="ew")
        ## Location Input Area
        # Labels
        tk.Label(self, text="Target Location:").grid(row=1, sticky="e")
        self.target_location_string = tk.StringVar()
        self.target_location_field = tk.Entry(self, textvariable=self.target_location_string, width=20)
        self.target_location_field.grid(row=1, column=1, sticky="we")

        ## Seach Area
        # Labels
        tk.Label(self, text="Identifier:").grid(row=2, sticky="e")
        
        # Entry
        self.search_string = tk.StringVar()
        self.search_field = tk.Entry(self, textvariable=self.search_string, width=20)
        self.search_field.grid(row=2, column=1, sticky="we")

        # Assign Button
        assignButton = tk.Button(self, text="Assign", width = 10, command=self.searchAndUpdate)
        assignButton.grid(row=3, column=1, sticky="w")

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
        self.serialNo = tk.Entry(self, textvariable=self.serialNumber_string, width=20, state=tk.DISABLED)
        self.phoneNo = tk.Entry(self, textvariable=self.phoneNumber_string, width=20, state=tk.DISABLED)
        self.iccid = tk.Entry(self, textvariable=self.iccid_string, width=20, state=tk.DISABLED)
        self.location = tk.Entry(self, textvariable=self.location_string, width=20, state=tk.DISABLED)

        # Field Properties
        self.imei.grid(row=4, column=1, sticky="we")
        self.serialNo.grid(row=5, column=1, sticky="we")
        self.phoneNo.grid(row=6, column=1, sticky="we")
        self.iccid.grid(row=7, column=1, sticky="we")
        self.location.grid(row=8, column=1, sticky="we")

        # Clear All Button
        self.cancelButton = tk.Button(self, text="Clear All", width = 5, command=self.clearEntries)
        self.cancelButton.grid(row=9, column=0, sticky="e")

        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready to seach...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=50, state='disabled')
        self.status.grid(row=10,column=0, columnspan=2, sticky="ws")

        # Binding
        self.target_location_field.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.search_field.bind("<Return>", self.searchAndUpdate)

        # Focus to search box
        self.target_location_field.focus()

    def clearEntries(self, event=None, clear_target_location_field=True):
        self.imei_string.set('')
        self.serialNumber_string.set('')
        self.phoneNumber_string.set('')
        self.iccid_string.set('')
        self.location_string.set('')

        if (clear_target_location_field):
            self.search_field.delete(0,'end')
            self.target_location_field.delete(0, 'end')
            self.target_location_field.focus()
        

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

            # Do not allow search with location or time
            if (column_definition[self.target_search_loc.col] == 'Location' or column_definition[self.target_search_loc.col] == 'Updated Time'):
                self.statusText.set("Cannot search with location or time!")
                return

            self.statusText.set("Found " + self.search_string.get() + " as " + column_definition[self.target_search_loc.col] + ".")

            # Update time and location
            worksheet.update_cell(self.target_search_loc.row, 1, time.time()) #time
            worksheet.update_cell(self.target_search_loc.row, 6, self.target_location_string.get()) #location
            
            # get the whole row
            row = worksheet.row_values(self.target_search_loc.row, value_render_option='UNFORMATTED_VALUE')

            # Clear search field
            self.search_field.delete(0, 'end')
            self.search_field.focus()

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

# GUI settings
root = tk.Tk()
app = App(root)
root.title("COVID-19 Tablet Location Update")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()