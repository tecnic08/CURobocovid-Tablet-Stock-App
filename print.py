import os
import imgkit
import pdfkit
from pystrich.datamatrix import DataMatrixEncoder
from components.thaiDateTime import *
from components.shipOutLetterFormat import *
from components.responseLetterFormat import *

def generateAndPrint(imei_str, serialNumber_str, phoneNumber_str, iccid_str, location_str, subLocation_str = '', deviceMode_str = '', copies = 1):
    imeiDataMatrix = DataMatrixEncoder(imei_str)
    imeiDataMatrix.save("imei.png")

    serialNumberDataMatrix = DataMatrixEncoder(serialNumber_str)
    serialNumberDataMatrix.save("serialNumber.png")

    iccidDataMatrix = DataMatrixEncoder(iccid_str)
    iccidDataMatrix.save("iccid.png")

    if (deviceMode_str != ''):
      deviceMode_str = deviceMode_str + ' Device'

    html_str = """
    <html>
    <body>
        <font face="Ubuntu">
          <table>
            <tr valign="middle">
                <td align="left"><img src = "imei.png"></td>
                <td><center>{0}<br/><br/>{1}</center></td>
                <td align="center"><h2>{4}</h2></td>
                <td align="center"><img src = "serialNumber.png"></td>
            </tr>
            <tr>
            </tr>
            <tr>
              <td rowspan="2"><img src = "iccid.png"></td>
              <td><center><b>Phone Number</b></center></td>
              <td colspan="2" rowspan="2"><center><h2>{2} {3}</h2></center></td>
            </tr>
            <tr>
              <td><center>{5}</center></td>
            </tr>
          </table>
        </font>
    </body>
    </html>""".format(imei_str, serialNumber_str, location_str, subLocation_str, deviceMode_str, phoneNumber_str)

    sticker_html= open("sticker.html","w")
    sticker_html.write(html_str)
    sticker_html.close()

    options = {'width': 490}
    imgkit.from_file('sticker.html', 'out.jpg', options=options)

    # Print
    printTerminalCommand = "lpr -P TSC_TE300 -o landscape"

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " out.jpg"

    os.system(printTerminalCommand)

    # Clean up
    os.remove("imei.png")
    os.remove("serialNumber.png")
    os.remove("iccid.png")
    os.remove("sticker.html")
    #os.remove("out.jpg")
    return

def printAddressLabel(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str, copies = 1):
    
    html_str = """
    <html>
    <body>
        <font face="TH Sarabun New">
        <p style="font-size:25px; margin:0; padding:0"><b>{0} ({1})</b></p>
        <p style="font-size:20px; margin:0; padding:0">{2} {3} {4} {5}</p>
    </font>
    </body>
    </html>""".format(name_str, phoneNumber_str, hospitalName_str, address_str, province_str, zipcode_str)

    sticker_html= open("address.html","w")
    sticker_html.write(html_str)
    sticker_html.close()

    options = {'width': 490, 'encoding':'utf8'}
    imgkit.from_file('address.html', 'address_label.jpg', options=options)

    # Print
    printTerminalCommand = "lpr -P TSC_TE300"

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " address_label.jpg"

    os.system(printTerminalCommand)

    # Clean up
    #os.remove("address.html")
    #os.remove("address_label.jpg")
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
    printTerminalCommand = "lpr -P HP-Color-LaserJet-MFP-M477fdw outLetter.pdf responseLetter.pdf"

    #os.system(printTerminalCommand)

    # # Clean up
    # os.remove("outLetter.html")
    # os.remove("outLetter.pdf")
    return