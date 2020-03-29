import os
import imgkit
from pystrich.datamatrix import DataMatrixEncoder

def generateAndPrint(imei_str, serialNumber_str, phoneNumber_str, iccid_str, location_str, copies = 1):
    imeiDataMatrix = DataMatrixEncoder(imei_str)
    imeiDataMatrix.save("imei.png")

    serialNumberDataMatrix = DataMatrixEncoder(serialNumber_str)
    serialNumberDataMatrix.save("serialNumber.png")

    iccidDataMatrix = DataMatrixEncoder(iccid_str)
    iccidDataMatrix.save("iccid.png")

    html_str = """
    <html>
    <body>
        <font face="Ubuntu">
          <table>
            <tr>
                <th rowspan="2"><img src = "imei.png"></th>
                <th><center><b>IMEI</b></center></th>
                <th><center><b>Serial Number</b></center></th>
                <th rowspan="2"><img src = "serialNumber.png"></th>
            </tr>
            <tr>
                <td><center>{0}</center></td>
                <td><center>{1}</center></td>
            </tr>
            <tr>
              <td rowspan="2"><img src = "iccid.png"></td>
              <td><center><b>Phone Number</b></center></td>
              <td colspan="2" rowspan="2"><center><h2>{2}</h2></center></td>
            </tr>
            <tr>
              <td><center>{3}</center></td>
            </tr>
          </table>
        </font>
    </body>
    </html>""".format(imei_str, serialNumber_str, location_str, phoneNumber_str)

    sticker_html= open("sticker.html","w")
    sticker_html.write(html_str)
    sticker_html.close()

    options = {'width': 490}
    imgkit.from_file('sticker.html', 'out.jpg', options=options)

    # Print
    printTerminalCommand = "lpr -P QL800 -o landscape"

    for x in range(copies):
      printTerminalCommand = printTerminalCommand + " out.jpg"

    os.system(printTerminalCommand)

    # Clean up
    os.remove("imei.png")
    os.remove("serialNumber.png")
    os.remove("iccid.png")
    os.remove("sticker.html")
    os.remove("out.jpg")
    return