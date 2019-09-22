from bottle import *
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat,TextFormat,Color
from gspread_formatting import format_cell_ranges

# sunstone API/history section
Api = "https://omt-hq.sunstone-cloud.com/tagdata/history" # Api you get data from

        # Excell sheet section
sheet_name=" test Api"
scope = ['https://www.googleapis.com/auth/drive']

        # Query parameters
# tagId = 65501
property_equal = "accelerometer"
timeformat = "msFromEpoch"
#from_msFromEpoch = -60000


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Access-Control-Allow-Headers'] = 'content-type'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'

@route('<any:path>', method='OPTIONS')
def response_for_options(**kwargs):
    return {}

@route('/getdata/<LoLaNid>',methd='GET')
def GetData(LoLaNid):
    Query_String = {'tagId': LoLaNid, "property_equal": property_equal, "timeformat": timeformat}
    from_msFromEpoch=request.query.from_msFromEpoch
    if  from_msFromEpoch:
        Query_String["from_msFromEpoch"]=from_msFromEpoch
    else :
        return "Wrong URL"

                #Query and resoponse
    response = requests.get(Api, Query_String)#Send the request and recieve the response
    data=response.json()# convert the response body into JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name('account_key.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    try:
       sheet.get_all_records() #if it is empty it will throw an exception
    except:
        sheet.append_row(['tagID','timeStamp','acceX','acceY','acceZ','gX','gY','gZ','mX','mY','mZ','t','p'])
        fmt = CellFormat(
            backgroundColor=Color(1, 0.9, 0.9),
            textFormat=TextFormat(bold=True),
            horizontalAlignment='CENTER')
        format_cell_ranges(sheet, [('A1:M1', fmt)])

    for x in range(len(data)):
        accX=int(round( (data[x]['value'][0]*1000)))
        accY = int(round((data[x]['value'][1] * 1000)))
        accZ = int(round((data[x]['value'][2] * 1000)))
        sheet.append_row([data[x]['tagId'],(data[x]['updatedAt_msFromEpoch']),accX,accY,accZ,0,0,0,0,0,0,0,0])
    return "done, data are in saved on "+sheet_name+"google sheet "

if __name__=='__main__':
    run(host='localhost', port=8080, debug=True)
