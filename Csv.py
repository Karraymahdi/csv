import csv
import requests
from bottle import *
import requests

# API section
Api = ""
# name of csv file
filename = "sunstone.csv"
# Query parameters

property_equal = "accelerometer"
timeformat = "msFromEpoch"

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

    print(Query_String)
    #Query and resoponse
    response = requests.get(Api, Query_String)#Send the request and recieve the response
    data=response.json()# convert the response body into JSON
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(['tagID','timeStamp','acceX','acceY','acceZ','gX','gY','gZ','mX','mY','mZ','t','p'])
        for x in range(len(data)):
            accX = int(round((data[x]['value'][0] * 1000)))
            accY = int(round((data[x]['value'][1] * 1000)))
            accZ = int(round((data[x]['value'][2] * 1000)))
            csvwriter.writerow([data[x]['tagId'], data[x]['updatedAt_msFromEpoch'],accX,accY,accZ,0,0,0,0,0,0,0,0])
    return "done"
if __name__ == '__main__':
        run(host='localhost', port=8080, debug=True)
