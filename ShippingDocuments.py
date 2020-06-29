#!/usr/bin/env python3

import tkinter as tk
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
sheet = client.open(shippingDatabase)

# Extract and print all of the values
worksheet = sheet.worksheet("computerReadable")

print("Connected to " + shippingDatabase)

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(anchor="w")

        self.selectedHospital = tk.StringVar(self)
        self.attnName = tk.StringVar(self)
        self.phoneNumber = tk.StringVar(self)
        self.doctorTablet = tk.StringVar(self)
        self.patientTablet = tk.StringVar(self)
        self.pinto = tk.StringVar(self)
        self.bestowed = tk.StringVar(self)
        self.documentNumber = tk.StringVar(self)

        #not showing
        self.address = tk.StringVar(self)
        self.province = tk.StringVar(self)
        self.postalCode = tk.StringVar(self)

        tk.Label(self, text="Hospital:").grid(row = 1, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.selectedHospital, width=40).grid(row = 1, column = 1, sticky = 'w')

        tk.Button(self, text="<<", command=self.goBackOneRecord).grid(row = 2, column = 0, sticky = 'w')
        tk.Button(self, text=">>", command=self.goForwardOneRecord).grid(row = 2, column = 0, sticky = 'e')
        tk.Button(self, text="Load Latest", command=self.searchAndLoadData).grid(row = 2, column = 1, sticky = 'e')
        tk.Button(self, text="Autorun", command=self.autoGenerate).grid(row = 2, column = 1, sticky = 'w')

        tk.Label(self, text="Attn:").grid(row = 3, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.attnName, width=40).grid(row = 3, column = 1, sticky = 'w')

        tk.Label(self, text="Phone No.:").grid(row = 4, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.phoneNumber, width=40).grid(row = 4, column = 1, sticky = 'w')

        self.printMirror = tk.IntVar()
        self.printMirror.set(1)
        checkButton = tk.Checkbutton(self, text="Print", variable=self.printMirror)
        checkButton.grid(row = 5, column = 1, rowspan = 2, sticky="e")

        tk.Label(self, text="Doctor Tablet:").grid(row = 5, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.doctorTablet, width=32).grid(row = 5, column = 1, sticky = 'w')

        tk.Label(self, text="Patient Tablet:").grid(row = 6, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.patientTablet, width=32).grid(row = 6, column = 1, sticky = 'w')

        self.printPinto = tk.IntVar()
        self.printPinto.set(1)
        checkButton = tk.Checkbutton(self, text="Print", variable=self.printPinto)
        checkButton.grid(row = 7, column = 1, sticky="e")

        tk.Label(self, text="Pinto:").grid(row = 7, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.pinto, width=32).grid(row = 7, column = 1, sticky = 'w')

        tk.Label(self, text="Document Number:").grid(row = 8, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.documentNumber, width=40).grid(row = 8, column = 1, sticky = 'w')

        tk.Label(self, text="Bestowed:").grid(row = 9, column = 0, sticky = 'e')
        tk.Entry(self, textvariable=self.bestowed, width=40).grid(row = 9, column = 1, sticky = 'w')

        # Print Addess
        self.printAddressLabel = tk.IntVar()
        self.printAddressLabel.set(1)
        checkButton = tk.Checkbutton(self, text="Print Address", variable=self.printAddressLabel)
        checkButton.grid(row=10, column = 1, sticky="w")

        # Print Documents
        self.printDocuments = tk.IntVar()
        self.printDocuments.set(1)
        checkButton = tk.Checkbutton(self, text="Print Documents", variable=self.printDocuments)
        checkButton.grid(row=10, column = 1, sticky="e")

        tk.Button(self, text="Print Selected Documents", command=self.sendPrintCommand).grid(row = 11, column = 1, sticky = 'e')
        tk.Button(self, text="Complete and Proceed", command=self.CompleteAndProceed).grid(row = 12, column = 1, sticky = 'e')

        self.searchAndLoadData()

    def clearEntries(self):
        self.selectedHospital.set("")
        self.attnName.set("")
        self.phoneNumber.set("")
        self.doctorTablet.set("")
        self.patientTablet.set("")
        self.address.set("")
        self.province.set("")
        self.postalCode.set("")
        self.documentNumber.set("")
        self.bestowed.set("")
        return

    def searchAndLoadData(self):
        try:
            # search for next hospital
            found_cell = worksheet.find(devicePreparedCursor)
            self.target_row = found_cell.row
            self.target_col = found_cell.col
            self.loadData()
            return True

        except:
            print("No cursor found! Using first row.")
            self.target_row = 2
            self.target_col = 1
            self.loadData()
            return False

    def loadData(self):
        try:
            self.clearEntries()
            hospital_row = worksheet.row_values(self.target_row, value_render_option='UNFORMATTED_VALUE')

            # fill in the data
            self.selectedHospital.set(hospital_row[2])
            self.attnName.set(hospital_row[3])
            self.phoneNumber.set(hospital_row[4])
            self.address.set(hospital_row[5])
            self.province.set(hospital_row[6])
            self.postalCode.set(hospital_row[7])
            self.doctorTablet.set(hospital_row[8])
            self.patientTablet.set(hospital_row[9])
            self.documentNumber.set(hospital_row[14])
            self.pinto.set(hospital_row[16])

            if (hospital_row[12] == 1):
                bestowedText = "Yes"
            else:
                bestowedText = "No"

            self.bestowed.set(bestowedText)
            return
        
        except:
            print("Something's wrong")
            return

    def goBackOneRecord(self):
        try:
            if(self.target_row > 2):
                self.target_row -= 1
                self.loadData()
                return

        except:
            print("Cannot Go Backward!")
            return

    def goForwardOneRecord(self):
        try:
            self.target_row += 1
            self.loadData()
            return

        except:
            print("Cannot Go Forward!")
            return

    def sendPrintCommand(self):
        if(self.printAddressLabel.get() == 1):
            printAddressLabel(self.attnName.get(), self.phoneNumber.get(), self.selectedHospital.get(), \
                self.address.get(), self.province.get(), self.postalCode.get(), self.bestowed.get(), copies=2)

        chaiPattana = False
        if (self.bestowed.get() == "Yes"):
            chaiPattana = True

        if(self.printDocuments.get() == 1):
            printDocuments(self.selectedHospital.get(), self.patientTablet.get(), self.doctorTablet.get(), \
                self.pinto.get(), chaiPattana, self.documentNumber.get(), bool(self.printMirror.get()), bool(self.printPinto.get()))
        return

    def CompleteAndProceed(self):
        worksheet.update_cell(self.target_row, self.target_col, documentPrintedCursor)
        self.searchAndLoadData()
        return

    def autoGenerate(self):
        while self.searchAndLoadData():
            self.sendPrintCommand()
            worksheet.update_cell(self.target_row, self.target_col, documentPrintedCursor)
        return

# GUI settings
root = tk.Tk()
app = App(root)
root.title("Document Printing")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()