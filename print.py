import os
import imgkit
import pdfkit
from pathlib import Path
from pystrich.datamatrix import DataMatrixEncoder
from pystrich.code128 import Code128Encoder
from components.thaiDateTime import *
from components.shipOutLetterFormat import *
from components.shipOutLetterChaiPattanaFormat import *
from components.responseLetterFormat import *
from components.responseLetterChaiPattanaFormat import *
from components.tabletLabelFormat import *
from components.pintoLabelFormat import *
from components.pintoRemoteFPVLabel import *
from config import *

def generateAndPrint(imei_str, serialNumber_str, phoneNumber_str, iccid_str, location_str, subLocation_str = '', deviceMode_str = '', copies = 1, printSupportLabel = 'auto'):
    imeiDataMatrix = DataMatrixEncoder(imei_str)
    imeiDataMatrix.save("imei.png")

    serialNumberDataMatrix = DataMatrixEncoder(serialNumber_str)
    serialNumberDataMatrix.save("serialNumber.png")

    iccidCode128 = Code128Encoder(iccid_str, options = {"show_label" : False})
    iccidCode128.save("iccid.png")

    supportLabel = (deviceMode_str == "Doctor") and (printSupportLabel == "auto")

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

    options = {'page-width' : '80mm', 'page-height' : '50mm', 'margin-top': '0mm', 'margin-right': '0mm','margin-bottom': '0mm', 'margin-left': '0mm'}
    pdfkit.from_file('sticker.html', 'sticker.pdf', options=options)
    fileToPrint = "sticker.pdf"

    if (supportLabel):
      options = {'page-width' : '80mm', 'page-height' : '50mm', 'margin-top': '3mm', 'margin-right': '0mm','margin-bottom': '2mm', 'margin-left': '0mm', 'encoding':'utf8'}
      pdfkit.from_file("components/supportLabel.html", "supportLabel.pdf", options=options)
      fileToPrint = fileToPrint + " supportLabel.pdf"

    # Print
    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1 -# {2} {3}".format(tabletLabelPrinter, darknessLevel, copies, fileToPrint)
    os.system(printTerminalCommand)

    # Clean up
    os.remove("imei.png")
    os.remove("serialNumber.png")
    os.remove("iccid.png")
    os.remove("sticker.html")
    os.remove("sticker.pdf")

    if (supportLabel):
      os.remove("supportLabel.pdf")

    return

def printAddressLabel(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str, bestowed_yes_no, copies = 1):
    
    if (bestowed_yes_no == "Yes"):
      bestowed = "B"
    else:
      bestowed = "N"

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
          <tr>
            <td><p style="font-size:28px; font-weight:bold; margin:0; padding-right:5px; padding:0px;">{6}</p></td>
          </tr>
        </table>
    </font>
    </body>
    </html>""".format(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str, bestowed)

    sticker_html= open("address.html","w")
    sticker_html.write(html_str)
    sticker_html.close()

    options = {'page-width' : '90mm', 'page-height' : '38mm', 'margin-top': '2mm', 'margin-right': '2mm','margin-bottom': '2mm', 'margin-left': '2mm', 'encoding':'utf8'}
    pdfkit.from_file('address.html', 'address_label.pdf', options=options)

    # Print
    printTerminalCommand = "lpr -P {0} ".format(addressLabelPrinter)

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " address_label.pdf"

    os.system(printTerminalCommand)

    # Clean up
    os.remove("address.html")
    os.remove("address_label.pdf")
    return

def printDocuments(hospitalName, patientTabletAmount, doctorTabletAmount, chaiPattana, documentNumber = ""):

    letter = open("outLetter.html","w")

    thaiDate = thai_strftime(datetime.datetime.now(), "%d %B %y")
    if (chaiPattana):
      letter.write(outLetterChaiPattana.format(hospitalName, patientTabletAmount, doctorTabletAmount, thaiDate, documentNumber))
    else:
      letter.write(outLetter.format(hospitalName, patientTabletAmount, doctorTabletAmount, thaiDate, documentNumber))
    letter.close()

    response = open("responseLetter.html","w")
    if (chaiPattana):
      response.write(responseLetterChaiPattana.format(hospitalName, patientTabletAmount, doctorTabletAmount))
    else:
      response.write(responseLetter.format(hospitalName, patientTabletAmount, doctorTabletAmount))
    response.close()

    Path("./outLetter").mkdir(parents=True, exist_ok=True)
    Path("./responseLetter").mkdir(parents=True, exist_ok=True)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'zoom' : 1.5
    }
    pdfkit.from_file('outLetter.html', 'outLetter/{}.pdf'.format(hospitalName), options=options)
    pdfkit.from_file('responseLetter.html', "responseLetter/{}.pdf".format(hospitalName), options=options)

    # Print
    printTerminalCommand = "lpr -P {0} \"outLetter/{1}.pdf\" \"responseLetter/{1}.pdf\"".format(standardA4Printer, hospitalName)

    os.system(printTerminalCommand)

    # Clean up
    os.remove("responseLetter.html")
    os.remove("outLetter.html")
    return

def printPintoSerialNumberLabel(serialNumber, videoGroup, controlNumber, copies = 1):
    serialNumberDataMatrix = DataMatrixEncoder(serialNumber)
    serialNumberDataMatrix.save("pintoSNDataMatrix.png")

    sticker_html= open("pintoSticker.html","w")
    sticker_html.write(pintoLabel.format(serialNumber, videoGroup, controlNumber))
    sticker_html.close()

    options = {'page-width' : '80mm', 
               'page-height' : '50mm',
               'margin-top': '0mm',
               'margin-right': '0mm',
               'margin-bottom': '0mm',
               'margin-left': '0mm',
               'encoding' : 'utf8'}
    pdfkit.from_file('pintoSticker.html', 'pintoSticker.pdf', options=options)
    fileToPrint = "pintoSticker.pdf"

    # Print
    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1 -# {2} {3}".format(tabletLabelPrinter, darknessLevel, copies, fileToPrint)
    os.system(printTerminalCommand)

    # Clean up
    os.remove("pintoSNDataMatrix.png")
    os.remove("pintoSticker.html")
    os.remove("pintoSticker.pdf")

    return

def printPintoRemoteSerialNumberLabel(serialNumber, videoGroup, copies = 1):
    serialNumberDataMatrix = DataMatrixEncoder(serialNumber)
    serialNumberDataMatrix.save("pintoSNDataMatrix.png")

    sticker_html= open("pintoRemoteLabel.html","w")
    sticker_html.write(pintoRemoteFPVLabel.format(serialNumber, videoGroup))
    sticker_html.close()

    options = {'page-width' : '100mm', 
               'page-height' : '25mm',
               'margin-top': '0mm',
               'margin-right': '0mm',
               'margin-bottom': '0mm',
               'margin-left': '0mm',
               'encoding' : 'utf8',
               'zoom':'0.57'}
    pdfkit.from_file('pintoRemoteLabel.html', 'pintoRemoteLabel.pdf', options=options)
    fileToPrint = "pintoRemoteLabel.pdf"

    # Print
    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1 -# {2} {3}".format(tabletLabelPrinter, darknessLevel, copies, fileToPrint)
    os.system(printTerminalCommand)

    # Clean up
    os.remove("pintoSNDataMatrix.png")
    os.remove("pintoRemoteLabel.html")
    os.remove("pintoRemoteLabel.pdf")

    return