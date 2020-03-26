#!/usr/bin/env python3

import tkinter as tk
import csv
import time
from csv import writer

# This app does not create the column name, please name it your self
CSV_FILE = "data.csv"

def popup(title, msg):
    '''Open popup window with title and msg'''
    w = tk.Toplevel(root)
    w.title(title)
    w.minsize(200, 200)
    tk.Label(w, text=msg).pack()
    tk.Button(w, text="Close", command=w.destroy).pack(pady=10)
    w.bind("<Return>", lambda f: w.destroy())

def read_from_file():
    try:
        devices = []
        with open(CSV_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                devices.append(row)

            return devices
    except IOError:
        popup("Error", "File not found!")

def write_to_file(device_list):
    with open(CSV_FILE, 'w') as f:
        csv.writer(f).writerows(device_list)

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(anchor="w")

        ## Seach Area
        # Labels
        tk.Label(self, text="IMEI Search and Update").grid(row=0, columnspan=2, sticky="ew")
        tk.Label(self, text="IMEI:").grid(row=1, sticky="e")

        # Search Button
        search = tk.Button(self, text="Search", width = 10, command=self.search)
        search.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Serial Number:").grid(row=4,sticky="e")
        tk.Label(self, text="Phone Number:").grid(row=5, sticky="e")
        tk.Label(self, text="ICCID:").grid(row=6, sticky="e")
        tk.Label(self, text="Deployed Location:").grid(row=7, sticky="e")

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
        self.imei.grid(row=1, column=1, sticky="we")
        self.serialNo.grid(row=4, column=1, sticky="we")
        self.phoneNo.grid(row=5, column=1, sticky="we")
        self.iccid.grid(row=6, column=1, sticky="we")
        self.location.grid(row=7, column=1, sticky="we")

        # Update Button
        update = tk.Button(self, text="Update", width = 10, command=self.update)
        update.grid(row=8, column=1, sticky="w")

        # Status Text
        self.statusText = tk.StringVar()
        self.statusText.set("Ready to seach...")
        self.status = tk.Entry(self, textvariable=self.statusText, width=50, state='disabled')
        self.status.grid(row=9,column=0, columnspan=2, sticky="ws")

        # Binding
        self.imei.bind("<Return>", self.search)

        self.serialNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.phoneNo.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.iccid.bind("<Return>", lambda x:root.event_generate('<Tab>'))
        self.location.bind("<Return>", self.update)

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

    def search(self, event=None):
        '''[updatedTime,serialNumber,imei,phoneNumber,iccid,deployedLocation]'''
        device_list  = read_from_file()

        if not device_list:
            return

        for row in device_list:
            if row[2] == self.imei_string.get():
                self.serialNumber_string.set(row[1])
                self.phoneNumber_string.set(row[3])
                self.iccid_string.set(row[4])
                self.location_sting.set(row[5])
                self.statusText.set("Found " + self.imei_string.get())
                return
        else:
            self.statusText.set(self.imei_string.get() + " NOT found")
            return
    
    def update(self, event=None):
        device_list  = read_from_file()

        if not device_list:
            return
            
        for row in device_list:
            if row[2] == self.imei_string.get():
                row[0] = time.time()
                row[1] = self.serialNumber_string.get()
                row[3] = self.phoneNumber_string.get()
                row[4] = self.iccid_string.get()
                row[5] = self.location_sting.get()
                self.statusText.set("Updated " + self.imei_string.get())
                break

        write_to_file(device_list)
        
        self.clearEntries()



# GUI settings
root = tk.Tk()
app = App(root)
root.title("COVID-19 Tablet CSV Generator")
root.minsize(200, 200)

# Initalize GUI
root.mainloop()