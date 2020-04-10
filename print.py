import os
import imgkit
from pystrich.datamatrix import DataMatrixEncoder

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

    # # Print
    # printTerminalCommand = "lpr -P QL800 -o landscape"

    # for x in range(copies):
    #   printTerminalCommand = printTerminalCommand + " out.jpg"

    # os.system(printTerminalCommand)

    # # Clean up
    # os.remove("imei.png")
    # os.remove("serialNumber.png")
    # os.remove("iccid.png")
    # os.remove("sticker.html")
    # os.remove("out.jpg")
    return