#!/usr/bin/env python3

import tkinter as tk
import csv
import time
from csv import writer

# This app does not create the column name, please name it your self
CSV_FILE = "data.csv"

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(anchor="w")

        # Labels
        tk.Label(self, text="IMEI:").grid(row=0, sticky="e")
        tk.Label(self, text="Serial Number:").grid(row=1,sticky="e")
        tk.Label(self, text="Phone Number:").grid(row=2, sticky="e")
        tk.Label(self, text="ICCID:").grid(row=3, sticky="e")
        tk.Label(self, text="Deployed Location:").grid(row=4, sticky="e")

        # Entries
        self.serialNumber_string = tk.StringVar()
        self.imei_string = tk.StringVar()
        self.phoneNumber_string = tk.StringVar()
        self.iccid_string = tk.StringVar()
        self.location_sting = tk.StringVar()

        # Entries Field
        self.imei = tk.Entry(self, textvariable=self.imei_string, width=20)
        self.serialNo = tk.Entry(self, textvariable=self.serialNumber_string, width=20)
        self.phoneNo = tk.Entry(self, textvariable=self.phoneNumber_string, width=20)
        self.iccid = tk.Entry(self, textvariable=self.iccid_string, width=20)
        self.location = tk.Entry(self, textvariable=self.location_sting, width=20)

        # Field Properties
        self.imei.grid(row=0, column=1, sticky="we")
        self.serialNo.grid(row=1, column=1, sticky="we")
        self.phoneNo.grid(row=2, column=1, sticky="we")
        self.iccid.grid(row=3, column=1, sticky="we")
        self.location.grid(row=4, column=1, sticky="we")

        # Add Button
        add = tk.Button(self, text="Add", width = 10, command=self.addRowToCSV)
        add.grid(row=5, column=1, sticky="w")

        # Clear Button
        clear = tk.Button(self, text="Clear", command=self.clearEntries)
        clear.grid(row=5, column=0, sticky="e")
        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready for input...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=50, state='disabled')
        self.status.grid(row=6,column=0, columnspan=2, sticky="ws")

        # Binding
        self.imei.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.serialNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.phoneNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.iccid.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.location.bind("<Return>", self.addRowToCSV)

        self.imei.focus()
        

    def addRowToCSV(self, event=None):
        addedTime = time.time()
        imei = self.imei_string.get()
        serialNo = self.serialNumber_string.get()
        phoneNo = self.phoneNumber_string.get()
        iccid = self.iccid_string.get()
        location = self.location_sting.get()

        # Do not write to csv if any of the field is empty
        if (imei == ''):
            self.statusText.set("Data NOT added! Please fill in IMEI! Ready for input...")
            return

        if (len(imei) != 15):
            self.statusText.set("Data NOT added! IMEI must be 15 digits")
            return


        with open(CSV_FILE, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow([addedTime, serialNo, imei, phoneNo, iccid, location])

        self.statusText.set("Added " + imei + ". Ready for input...")
        self.clearEntries()

    def clearEntries(self, event=None):
        self.imei.delete(0, 'end')
        self.serialNo.delete(0, 'end')
        self.phoneNo.delete(0, 'end')
        self.location.delete(0, 'end')
        self.iccid.delete(0,'end')
        self.imei.focus()


# GUI settings
root = tk.Tk()
app = App(root)
root.title("COVID-19 Tablet CSV Generator")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()