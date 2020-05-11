#!/usr/bin/env python3
import os
import pdfkit
import gspread
from pathlib import Path
from pystrich.datamatrix import DataMatrixEncoder
from oauth2client.service_account import ServiceAccountCredentials
from components.thaiDateTime import *
from components.pintoLabelFormat import *
from components.pintoRemoteFPVLabel import *
from config import *

def createPintoLabel(serialStart, serialEnd, videoStart, lotName):
    videoGroup = {
        0 : "D",    # We will use mod, so last group must be ZERO
        1 : "A",
        2 : "B",
        3 : "C"
    }

    for serialNumber in range(serialStart, serialEnd + 1):
        generatePintoSerialNumberLabel(serialNumber, videoGroup[videoStart % len(videoGroup)], lotName)
        generatePintoRemoteSerialNumberLabel(serialNumber, videoGroup[videoStart % len(videoGroup)])
        videoStart += 1

    return

def generatePintoSerialNumberLabel(serialNumber, videoGroup, controlNumber):
    serialNumberDataMatrix = DataMatrixEncoder(str(serialNumber))
    serialNumberDataMatrix.save("pintoSNDataMatrix.png")

    sticker_html= open("pintoSticker.html","w")
    sticker_html.write(pintoLabel.format(serialNumber, videoGroup, controlNumber))
    sticker_html.close()

    outputFileName = "pintoLabel/pinto{0}.pdf".format(serialNumber)

    options = {'page-width' : '80mm', 
               'page-height' : '50mm',
               'margin-top': '0mm',
               'margin-right': '0mm',
               'margin-bottom': '0mm',
               'margin-left': '0mm',
               'encoding' : 'utf8'}
    pdfkit.from_file('pintoSticker.html', outputFileName, options=options)

    # Clean up
    os.remove("pintoSNDataMatrix.png")
    os.remove("pintoSticker.html")
    return

def generatePintoRemoteSerialNumberLabel(serialNumber, videoGroup, copies = 1):
    serialNumberDataMatrix = DataMatrixEncoder(str(serialNumber))
    serialNumberDataMatrix.save("pintoSNDataMatrix.png")

    sticker_html= open("pintoRemoteLabel.html","w")
    sticker_html.write(pintoRemoteFPVLabel.format(serialNumber, videoGroup))
    sticker_html.close()

    outputFileName = "pintoLabel/remote{0}.pdf".format(serialNumber)

    options = {'page-width' : '100mm', 
               'page-height' : '25mm',
               'margin-top': '0mm',
               'margin-right': '0mm',
               'margin-bottom': '0mm',
               'margin-left': '0mm',
               'encoding' : 'utf8',
               'zoom':'0.57'}

    pdfkit.from_file('pintoRemoteLabel.html', outputFileName, options=options)

    # Clean up
    os.remove("pintoSNDataMatrix.png")
    os.remove("pintoRemoteLabel.html")

    return

def printPintoLabel(serialStart,serialEnd):

    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1".format(tabletLabelPrinter, darknessLevel)

    for serialNumber in range(serialStart, serialEnd + 1):
        printTerminalCommand =  printTerminalCommand + " pinto{0}.pdf".format(serialNumber)

    os.system(printTerminalCommand)
    return

def printRemoteLabel(serialStart,serialEnd):

    printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1".format(tabletLabelPrinter, darknessLevel)

    for serialNumber in range(serialStart, serialEnd + 1):
        printTerminalCommand =  printTerminalCommand + " pintoLabel/remote{0}.pdf".format(serialNumber)

    os.system(printTerminalCommand)
    return

# def createPintoLetter(startRow, endRow, printDocuments = False, sendOutLetter = True, replyLetter = True):

#     print("Connecting to Google Drive API...")
#     # use creds to create a client to interact with the Google Drive API
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(clientCredentialFile, scope)
#     client = gspread.authorize(creds)

#     # Find a workbook by name and open the first sheet
#     pintoShippingSheet = client.open(shippingDatabase)
#     pintoShippingWorksheet = pintoShippingSheet.worksheet("computerReadable-Pinto")
#     print("Connected to " + shippingDatabase)

#     fileToPrint = ""

#     for i in range(startRow, endRow + 1):
#         # get desired row
#         focusedRow = pintoShippingWorksheet.row_values(i)

#         # get Thai date text
#         thaiDateText = thai_strftime(datetime.datetime.now(), "%d %B %y")

#         # generate documents
#         if sendOutLetter:
#             fileToPrint += "\"{}\" ".format(generatePintoSendOutLetter(focusedRow(pintoColumn['hospitalName']),\
#                 focusedRow(pintoColumn['noOfPinto']),\
#                 focusedRow(pintoColumn['documentNumber']),\
#                 thaiDateText,\
#                 focusedRow(pintoColumn['chaipattana'])))

#         if replyLetter:
#             fileToPrint += "\"{}\" ".format(generatePintoReplyLetter(focusedRow(pintoColumn['hospitalName']),\
#                 focusedRow(pintoColumn['noOfPinto']),\
#                 focusedRow(pintoColumn['chaipattana'])))

#         print("Generated {} of {} document set.".format(i, (endRow - startRow)))

#     # print
#     if printDocuments and fileToPrint != "":
#         printTerminalCommand = "lpr -P {0} {1}".format(standardA4Printer, fileToPrint)
#         os.system(printTerminalCommand)
#         print("Print command has been sent to " + standardA4Printer)
    
#     print("Done!")

# def generatePintoSendOutLetter(hospitalName, noOfPinto, documentNo, date, chaiPattana):

#     letter = open("pintoOutLetter.html","w")

#     if (int(chaiPattana)):
#       letter.write(pintoSendOutLetterChaiPattana.format(hospitalName, noOfPinto, documentNo, date))
#     else:
#       letter.write(pintoSendOutLetter.format(hospitalName, noOfPinto, documentNo, date))
#     letter.close()

#     Path("./pintoSendOutLetter").mkdir(parents=True, exist_ok=True)

#     options = {
#         'page-size': 'A4',
#         'margin-top': '0.75in',
#         'margin-right': '0.75in',
#         'margin-bottom': '0.75in',
#         'margin-left': '0.75in',
#         'encoding': "UTF-8",
#         'zoom' : 1.5
#     }
#     outputFile = hospitalName + ".pdf"
#     pdfkit.from_file('pintoOutLetter.html', 'pintoSendOutLetter/{}'.format(outputFile), options=options)
    
#     return outputFile

# def generatePintoReplyLetter(hospitalName, noOfPinto, chaiPattana):

#     letter = open("pintoReplyLetter.html","w")

#     if (int(chaiPattana)):
#       letter.write(pintoReplyLetterChaiPattana.format(hospitalName, noOfPinto, documentNo, date))
#     else:
#       letter.write(pintoReplyLetter.format(hospitalName, noOfPinto, documentNo, date))
#     letter.close()

#     Path("./pintoReplyLetter").mkdir(parents=True, exist_ok=True)

#     options = {
#         'page-size': 'A4',
#         'margin-top': '0.75in',
#         'margin-right': '0.75in',
#         'margin-bottom': '0.75in',
#         'margin-left': '0.75in',
#         'encoding': "UTF-8",
#         'zoom' : 1.5
#     }
#     outputFile = hospitalName + "_reply.pdf"
#     pdfkit.from_file('pintoOutLetter.html', 'pintoReplyLetter/{}'.format(outputFile), options=options)
    
#     return outputFile