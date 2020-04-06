Installing Prerequisite
===
```
sudo apt update
sudo apt install python3 python3-pip python3-tkinter wkhtmltopdf
pip3 install gspread oauth2-client imgkit pyStrich
```

Signed Credentials
===
This program will not work without json credential file obtained from Google Developer Console.

Read *Google Drive API and Service Accounts* here on how to obtain ones: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

How-to use
===
Adding a tablet
---
Execute `python3 ./AddDataGSheet.py`

Prepare:
* Tablet IMEI
* Tablet Serial Number
* Phone Number
* SIM Card ICCID
* Mobile Operator Name
* *QL800 Label Printer (if you want to print a label)*

Use a barcode reader to scan the data one by one.

Setting location
---
Execute `python3 ./LocationSet.py`

Type in all the location information. Then, scan either IMEI / Serial Number / Phone Number / ICCID of the tablet and location will be set.