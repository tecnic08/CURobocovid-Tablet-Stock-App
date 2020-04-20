import os
import imgkit
import pdfkit
from pystrich.datamatrix import DataMatrixEncoder
from pystrich.code128 import Code128Encoder
from components.thaiDateTime import *
from components.shipOutLetterFormat import *
from components.responseLetterFormat import *
from components.tabletLabelFormat import *
from config import *

def generateAndPrint(imei_str, serialNumber_str, phoneNumber_str, iccid_str, location_str, subLocation_str = '', deviceMode_str = '', copies = 1):
    imeiDataMatrix = DataMatrixEncoder(imei_str)
    imeiDataMatrix.save("imei.png")

    serialNumberDataMatrix = DataMatrixEncoder(serialNumber_str)
    serialNumberDataMatrix.save("serialNumber.png")

    iccidCode128 = Code128Encoder(iccid_str, options = {"show_label" : False})
    iccidCode128.save("iccid.png")

    printSupportLabel = (deviceMode_str == "Doctor")

    # Add suffix to device
    if (deviceMode_str != ''):
      deviceMode_str = deviceMode_str + ' Device'

    # Add zero prefix and remove last digit from phone number
    if (phoneNumber_str != ''):
      phoneNumber_str = phoneNumber_str[:-1]
      phoneNumber_str = "0" + phoneNumber_str

    sticker_html= open("sticker.html","w")
    sticker_html.write(tabletLabel.format(imei_str, serialNumber_str, location_str, subLocation_str, deviceMode_str, phoneNumber_str))
    sticker_html.close()

    print(len(location_str)+len(subLocation_str))

    options = {'page-width' : '80mm', 'page-height' : '50mm', 'margin-top': '0mm', 'margin-right': '0mm','margin-bottom': '0mm', 'margin-left': '0mm'}
    pdfkit.from_file('sticker.html', 'sticker.pdf', options=options)

    # Print
    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1".format(tabletLabelPrinter, darknessLevel)

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " sticker.pdf"

    os.system(printTerminalCommand)

    if (printSupportLabel):
      options = {'page-width' : '80mm', 'page-height' : '50mm', 'margin-top': '3mm', 'margin-right': '0mm','margin-bottom': '2mm', 'margin-left': '0mm', 'encoding':'utf8'}
      pdfkit.from_file("components/supportLabel.html", "supportLabel.pdf", options=options)
      os.system(printTerminalCommand = "lpr -P {0} -o Darkness={1} supportLabel.pdf".format(tabletLabelPrinter, darknessLevel))
      os.remove("supportLabel.pdf")

    # Clean up
    os.remove("imei.png")
    os.remove("serialNumber.png")
    os.remove("iccid.png")
    os.remove("sticker.html")
    os.remove("sticker.pdf")

    return

def printAddressLabel(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str, copies = 1):
    
    html_str = """
    <html>
    <body>
        <font face="TH Sarabun New">
        <table style="width: 500px; height: 190px">
          <tr>
            <td><p style="font-size:35px; margin:0; padding:0; text-align:center"><b>{0} ({1})</b></p></td>
          </tr>
          <tr>
            <td><p style="font-size:28px; margin:0; padding:0; text-align:center">{2} {3} {4} {5}</p></td>
          </tr>
        </table>
    </font>
    </body>
    </html>""".format(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str)

    sticker_html= open("address.html","w")
    sticker_html.write(html_str)
    sticker_html.close()

    options = {'page-width' : '90mm', 'page-height' : '38mm', 'margin-top': '2mm', 'margin-right': '2mm','margin-bottom': '2mm', 'margin-left': '2mm', 'encoding':'utf8'}
    pdfkit.from_file('address.html', 'address_label.pdf', options=options)

    # Print
    printTerminalCommand = "lpr -P {0}".format(addressLabelPrinter)

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " address_label.pdf"

    os.system(printTerminalCommand)

    # Clean up
    os.remove("address.html")
    os.remove("address_label.pdf")
    return

def printDocuments(hospitalName, patientTabletAmount, doctorTabletAmount):

    letter = open("outLetter.html","w")
    thaiDate = thai_strftime(datetime.datetime.now(), "%d %B %y")
    letter.write(outLetter.format(hospitalName, patientTabletAmount, doctorTabletAmount, thaiDate))
    letter.close()

    response = open("responseLetter.html","w")
    response.write(responseLetter.format(hospitalName, patientTabletAmount, doctorTabletAmount))
    response.close()

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'zoom' : 1.5
    }
    pdfkit.from_file('outLetter.html', 'outLetter.pdf', options=options)
    pdfkit.from_file('responseLetter.html', 'responseLetter.pdf', options=options)

    # Print
    printTerminalCommand = "lpr -P {} outLetter.pdf responseLetter.pdf".format(standardA4Printer)

    os.system(printTerminalCommand)

    # Clean up
    os.remove("responseLetter.html")
    os.remove("responseLetter.pdf")
    os.remove("outLetter.html")
    os.remove("outLetter.pdf")
    return