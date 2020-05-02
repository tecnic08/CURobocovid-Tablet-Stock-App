#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as tkFont
import time
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
databaseSheet = client.open(useDatabase)
shippingSheet = client.open(shippingDatabase)

databaseWorksheet = databaseSheet.worksheet('DO NOT EDIT!')
shippingWorksheet = shippingSheet.worksheet("computerReadable")

print("Connected to " + useDatabase)

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
        #________________________
        #           |           |
        #|Fetch     |           |
        #|Target    |Search     |
        #|Hospital  |And        |
        #|From      |Assign     |
        #|Shipping  |Location   |
        #|Database  |           |
        #|__________|___________|


        ## Fetch Target Hospital

        # Data
        self.selectedHospital = tk.StringVar(self)
        self.attnName = tk.StringVar(self)
        self.phoneNumber = tk.StringVar(self)
        self.doctorTablet = tk.StringVar(self)
        self.patientTablet = tk.StringVar(self)
        self.address = tk.StringVar(self)
        self.province = tk.StringVar(self)
        self.postalCode = tk.StringVar(self)
        self.request = tk.StringVar(self)

        # Text Field
        tk.Label(self, text="Hospital:").grid(row = 1, column = 0, sticky = 'e')
        tk.Label(self, textvariable=self.selectedHospital, width=30).grid(row = 1, column = 1, sticky = 'w')

        tk.Button(self, text="Load Data", command=self.loadData).grid(row = 2, column = 1, sticky = 'e')

        tk.Label(self, text="Attn:").grid(row = 3, column = 0, sticky = 'e')
        tk.Label(self, textvariable=self.attnName, width=30).grid(row = 3, column = 1, sticky = 'w')

        tk.Label(self, text="Phone No.:").grid(row = 4, column = 0, sticky = 'e')
        tk.Label(self, textvariable=self.phoneNumber, width=30).grid(row = 4, column = 1, sticky = 'w')

        #tk.Button(self, text="Print Documents", command=self.printDocuments).grid(row = 5, column = 1, sticky = 'e')

        tk.Label(self, text="Patient Table").grid(row = 6, column = 1, sticky = 'w')
        tk.Label(self, textvariable=self.patientTablet, font=tkFont.Font(size=26)).grid(row = 7, rowspan = 3, column = 1, sticky = 'w')

        tk.Label(self, text="Doctor Tablet").grid(row = 6, column = 1, sticky = 'e')
        tk.Label(self, textvariable=self.doctorTablet, font=tkFont.Font(size=26)).grid(row = 7, rowspan = 3, column = 1, sticky = 'e')

        tk.Label(self, text="Request:").grid(row = 10, column = 0, sticky = 'e')
        tk.Label(self, textvariable=self.request, width=30).grid(row = 10, column = 1, sticky = 'w')

        

        ## Search and Assign Location

        tk.Label(self, text="Location Assignment").grid(row=0, column=2, columnspan=2, sticky="ew")

        # Labels
        tk.Label(self, text="Identifier:").grid(row=1, column=2, sticky="e")
        self.search_string = tk.StringVar()
        self.search_field = tk.Entry(self, textvariable=self.search_string, width=40)
        self.search_field.grid(row=1, column=3, sticky="we")

        ## Location Input Area
        tk.Label(self, text="Location").grid(row=2, column=2, columnspan=2, sticky="we")
        # Labels
        tk.Label(self, text="Target Location:").grid(row=3, column=2, sticky="e")
        self.target_location_string = tk.StringVar()
        self.target_location_field = tk.Entry(self, textvariable=self.target_location_string, width=40)
        self.target_location_field.grid(row=3, column=3, sticky="we")

        tk.Label(self, text="Sub Location:").grid(row=4, column=2, sticky="e")
        self.target_sub_location_string = tk.StringVar()
        self.target_sub_location_field = tk.Entry(self, textvariable=self.target_sub_location_string, width=40)
        self.target_sub_location_field.grid(row=4, column=3, sticky="we")
        
        tk.Label(self, text="Project:").grid(row=5, column=2, sticky="e")
        self.target_project_string = tk.StringVar()
        self.target_project_string.set(projectOptions[0])
        self.target_project_field = tk.OptionMenu(self, self.target_project_string, *projectOptions)
        self.target_project_field.grid(row=5, column=3, sticky="we")

        tk.Label(self, text="Device Mode:").grid(row=6, column=2, sticky="e")
        self.target_device_mode_string = tk.StringVar()
        self.target_device_mode_string.set(deviceModeOptions[0])
        self.target_device_mode_field = tk.OptionMenu(self, self.target_device_mode_string, *deviceModeOptions)
        self.target_device_mode_field.grid(row=6, column=3, sticky="we")

        # Assign Button
        assignButton = tk.Button(self, text="Assign", width = 10, command=self.searchAndUpdate)
        assignButton.grid(row=7, column=3, sticky="w")

        # Print Checkbox
        self.printCheck = tk.IntVar()
        self.printCheck.set(1)
        checkButton = tk.Checkbutton(self, text="Print Label", variable=self.printCheck)
        checkButton.grid(row=7, column = 3, sticky="e")


        ## Records
        tk.Label(self, text="Current Records").grid(row=8, column=2, columnspan=2,sticky="we")

        # Label
        tk.Label(self, text="IMEI:").grid(row=9, column=2, sticky="e")
        self.imei_string = tk.StringVar()
        self.imei = tk.Entry(self, textvariable=self.imei_string, width=40, state=tk.DISABLED)
        self.imei.grid(row=9, column=3, sticky="we")

        tk.Label(self, text="Serial Number:").grid(row=10, column=2, sticky="e")
        self.serialNumber_string = tk.StringVar()
        self.serialNo = tk.Entry(self, textvariable=self.serialNumber_string, width=40, state=tk.DISABLED)
        self.serialNo.grid(row=10, column=3, sticky="we")
        
        tk.Label(self, text="Cellular Information:").grid(row=11, column=2, sticky="e")
        self.cellularInfo_string = tk.StringVar()
        self.cellularInfo = tk.Entry(self, textvariable=self.cellularInfo_string, width=40, state=tk.DISABLED)
        self.cellularInfo.grid(row=11, column=3, sticky="we")
        
        tk.Label(self, text="Deployed Location:").grid(row=12, column=2, sticky="e")
        self.location_string = tk.StringVar()
        self.location = tk.Entry(self, textvariable=self.location_string, width=40, state=tk.DISABLED)
        self.location.grid(row=12, column=3, sticky="we")

        tk.Label(self, text="Device Mode:").grid(row=13, column=2, sticky="e")
        self.deviceMode_string = tk.StringVar()
        self.deviceMode = tk.Entry(self, textvariable=self.deviceMode_string, width=40, state=tk.DISABLED)
        self.deviceMode.grid(row=13, column=3, sticky="we")

        # Clear All Button
        self.cancelButton = tk.Button(self, text="Clear All", width = 5, command=self.clearEntries)
        self.cancelButton.grid(row=14, column=3, sticky="w")

        # Proceed Button
        tk.Button(self, text="Complete and Proceed", command=self.CompleteAndProceed).grid(row = 14, column = 3, sticky = 'e')

        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready to seach...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=100, state='disabled')
        self.status.grid(row=15,column=0, columnspan=4, sticky="ws")

        # Binding
        self.target_location_field.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.search_field.bind("<Return>", self.searchAndUpdate)

        # Focus to search box
        self.search_field.focus()

    def loadData(self):
        try:
            self.clearEntries()
            
            # search for next hospital
            self.found_cell = shippingWorksheet.find(nextInQueCursor)
            hospital_row = shippingWorksheet.row_values(self.found_cell.row, value_render_option='UNFORMATTED_VALUE')

            # fill in the data
            self.selectedHospital.set(hospital_row[2])
            self.attnName.set(hospital_row[3])
            self.phoneNumber.set(hospital_row[4])
            self.address.set(hospital_row[5])
            self.province.set(hospital_row[6])
            self.postalCode.set(hospital_row[7])
            self.doctorTablet.set(hospital_row[8])
            self.patientTablet.set(hospital_row[9])

            if(len(hospital_row) > 13):
                self.request.set(hospital_row[13])

            # fill in location field
            self.target_location_string.set(hospital_row[10])
            self.target_sub_location_string.set(hospital_row[11])

            self.statusText.set("Data Loaded")
            return
        
        except:
            print("Something's wrong")
            return

    # def printDocuments(self):
    #     if (self.selectedHospital.get() == ''):
    #         self.statusText.set("Cannot Print: Load Data First!")
    #         return

    #     printAddressLabel(self.attnName.get(), self.phoneNumber.get(), self.selectedHospital.get(), self.address.get(), self.province.get(), self.postalCode.get())
    #     printDocuments(self.selectedHospital.get(), self.patientTablet.get(), self.doctorTablet.get())
    #     return

    def CompleteAndProceed(self):
        try:
            shippingWorksheet.update_cell(self.found_cell.row, self.found_cell.col, devicePreparedCursor)
            shippingWorksheet.update_cell(self.found_cell.row + 1, self.found_cell.col, nextInQueCursor)
            self.loadData()
            self.statusText.set("Proceeded to next data in que.")
            return

        except AttributeError:
            self.statusText.set("Cannot Proceed: No Data Loaded!")
            return

    def clearEntries(self, event=None, clear_target_location_field=True, clear_que=True):
        try:
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

            if (clear_que):
                self.selectedHospital.set("")
                self.attnName.set("")
                self.phoneNumber.set("")
                self.doctorTablet.set("")
                self.patientTablet.set("")
                self.address.set("")
                self.province.set("")
                self.postalCode.set("")
                self.request.set("")
                del self.found_cell #can cause AttributeError (must be last operation)

            return
        
        except AttributeError:
            # should be from self.found_cell, that's fine
            return



    def searchAndUpdate(self, event=None):
        try:
            # Clear current result
            self.clearEntries(clear_target_location_field = False, clear_que=False)

            # Do not allow empty search
            if (len(self.search_string.get()) < 5):
                self.statusText.set("Search string too short!")
                return

            self.statusText.set("Searching...")
            self.target_search_loc = databaseWorksheet.find(self.search_string.get())

            # Only allow search with IMEI / SN / Phone Number / ICCID
            if (self.target_search_loc.col < 2 or self.target_search_loc.col > 5):
                self.statusText.set("Only accept IMEI / SN / Phone Number / ICCID")
                return

            self.statusText.set("Found " + self.search_string.get() + " as " + column_definition[self.target_search_loc.col] + ".")

            # Update time and location
            databaseWorksheet.update_cell(self.target_search_loc.row, 1, time.time()) #time
            databaseWorksheet.update_cell(self.target_search_loc.row, 6, self.target_location_string.get()) #location
            databaseWorksheet.update_cell(self.target_search_loc.row, 7, self.target_sub_location_string.get()) #sub location
            databaseWorksheet.update_cell(self.target_search_loc.row, 8, self.target_project_string.get()) #project
            databaseWorksheet.update_cell(self.target_search_loc.row, 9, self.target_device_mode_string.get()) #mode
            
            # get the whole row
            row = databaseWorksheet.row_values(self.target_search_loc.row, value_render_option='UNFORMATTED_VALUE')

            # Clear search field
            self.search_field.delete(0, 'end')
            self.search_field.focus()

            # decode row
            imei_str = row[1]
            sn_str = row[2]
            phoneNumber_str = row[3]
            iccid_str = row[4]
            location_str = row[5]
            subLocation_str = row[6]
            project_str = row[7]
            deviceMode_str = row[8]
            operator_str = row[9]

            # update each field for displaying
            self.imei_string.set(imei_str)
            self.serialNumber_string.set(sn_str)
            self.cellularInfo_string.set("0{} / {}".format(phoneNumber_str, operator_str))
            self.location_string.set("{} {}".format(location_str, subLocation_str))
            self.deviceMode_string.set("{} {}".format(project_str, deviceMode_str))

            if (self.printCheck.get() == 1):
                generateAndPrint(imei_str, sn_str, phoneNumber_str, iccid_str, location_str, subLocation_str, deviceMode_str, 1)

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
root.title("COVID-19 Tablet Location Set and Print")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()