#!/usr/bin/env python3
import os
import pdfkit
from pystrich.datamatrix import DataMatrixEncoder
from components.pintoLabelFormat import *
from components.pintoRemoteFPVLabel import *
from config import *

def createPintoLabel(serialStart, serialEnd, videoStart, lotName, print=False):
    videoGroup = {
        0 : "D",    # We will use mod, so last group must be ZERO
        1 : "A",
        2 : "B",
        3 : "C"
    }

    #printTerminalCommand = "lpr -P {0} -o Darkness={1} -o page-ranges=1".format(tabletLabelPrinter, darknessLevel)

    for serialNumber in range(serialStart, serialEnd + 1):
        generatePintoSerialNumberLabel(serialNumber, videoGroup[videoStart % len(videoGroup)], lotName)
        generatePintoRemoteSerialNumberLabel(serialNumber, videoGroup[videoStart % len(videoGroup)])
        videoStart += 1
        #printTerminalCommand =  printTerminalCommand + " pinto{0}.pdf".format(serialNumber) + " remote{0}.pdf".format(serialNumber)
    
    #if(print):
    #    os.system(printTerminalCommand)

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