# Printer Configuration
tabletLabelPrinter = 'TE210'
addressLabelPrinter = 'QL800'
standardA4Printer = 'HP-Color-LaserJet-MFP-M477fdw'

# TSC Printer Darkness
darknessLevel = '14'

# Database Location
developmentDatabase = 'Tablet Database Dev'
productionDatabase = 'COVID-19 Tablet DB'

# Database to use
useDatabase = productionDatabase

# Shipping Database Location
shippingDatabase = 'แบบแสดงความต้องการชุดระบบสื่อสารทางไกล (การตอบกลับ)'

# Client Credential
clientCredentialFile = 'client_secret.json'

# Cellular Operator Number Prefix
cellularOperatorPrefix = {
    0 : 'TrueMove',
    3 : 'AIS'
}

# Shipping cursor
nextInQueCursor = "nextInQue"
devicePreparedCursor = "deviceReady"
documentPrintedCursor = "documentPrinted"

# Database
column_definition = {
    1: 'Updated Time',
    2: 'IMEI',
    3: 'Serial Number',
    4: 'Phone Number',
    5: 'ICCID',
    6: 'Location',
    7: 'Sub Location',
    8: 'Project',
    9: 'Mode',
    10: 'Cellular Operator'
}

deviceModeOptions = [
    'Patient',
    'Doctor',
    'Development',
    'Undefined'
]

projectOptions = [
    'Telepresence',
    'Pinto',
    'Development',
    'Undefined'
]

# Pinto shipping database

pintoColumn = {
    'status' : 0,
    'shipDate' : 1,
    'hospitalName' : 2,
    'attn' : 3,
    'phoneNumber' : 4,
    'address' : 5,
    'province' : 6,
    'postalCode' : 7,
    'noOfPinto' : 8,
    'chaipattana' : 9,
    'documentNumber' : 10
}