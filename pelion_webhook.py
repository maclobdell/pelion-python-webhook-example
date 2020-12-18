#!/usr/bin/python3
import sys, pycurl, certifi
from io import BytesIO

#setup a Pelion webhook notification channel to monitor a resource from a group of devices

def main(argv):

    #get api keys and webhook callback url from command line argument
    if len(sys.argv) > 2:
        api_key = argv[0]   #pelion access key
        aws_api_key = argv[1] #aws access key
        aws_callback_url = argv[2] #aws webhook callback url (without https://)

    else:
        print("Error: please pass API KEYs")
        sys.exit()

    create_webhook(api_key, aws_api_key, aws_callback_url)

    resource_uri = '/3200/0/5501'  #digital counter resource used in mbed-os-example-pelion

    subscribe_to_resource(api_key, resource_uri)


def create_webhook(api_key,aws_api_key, aws_callback_url):

    #enable webhook notification channel

    print("CREATE WEBHOOK")

    # curl -X PUT https://api.us-east-1.mbedcloud.com/v2/notification/callback \
    # -H 'Authorization: Bearer PELION_API_KEY' \
    # -H 'content-type: application/json' \
    # -d '{
    # "url": "AWS_API_ENDPOINT",
    # "headers": { "x-api-key": "AWS_API_KEY"}
    # }'

    #prepare request and buffer for response
    buffer = BytesIO()
    header = []
    header.append("Authorization: Bearer " + api_key)
    header.append("content-type: application/json")
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.us-east-1.mbedcloud.com/v2/notification/callback')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.NOPROGRESS,1)
    c.setopt(c.NOBODY,1)
    c.setopt(c.HEADER,1)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.TCP_KEEPALIVE,1)

    #data = '{"url": "https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/default/xxxxxxxxxxxxx","headers": { "x-api-key": "' + aws_api_key + '"}}'
    data = '{"url": "https://' + aws_callback_url + '","headers": { "x-api-key": "' + aws_api_key + '"}}'

    dbuffer = BytesIO(data.encode('utf-8'))
    c.setopt(c.UPLOAD, 1)
    c.setopt(c.READDATA, dbuffer)
    print(data)

    #execute request
    c.perform()
    c.close()

    #print response
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))


def subscribe_to_resource(api_key,resource_uri):

    #subscribe to a specific resource on any endpoint connected to your account

    # curl -X PUT https://api.us-east-1.mbedcloud.com/v2/subscriptions \
    # -H 'Authorization: Bearer PELION_API_KEY' \
    # -H 'content-type: application/json' \
    # -d '[
    #        {
    #          "endpoint-name": "*",
    #          "resource-path": ["/object/instance/resource", ... ] 
    #        }
    #     ]'

    print("SUBSCRIBE TO RESOURCE: " + resource_uri) 
    
    #prepare request and buffer for response
    buffer = BytesIO()
    header = []
    header.append("Authorization: Bearer " + api_key)

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.us-east-1.mbedcloud.com/v2/subscriptions/')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.NOPROGRESS,1)
    c.setopt(c.NOBODY,1)
    c.setopt(c.HEADER,1)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.TCP_KEEPALIVE,1)

    data = '[{"endpoint-name": "*","resource-path": ["' + resource_uri + '"]}]'

    print(data)

    dbuffer = BytesIO(data.encode('utf-8'))
    c.setopt(c.UPLOAD, 1)
    c.setopt(c.READDATA, dbuffer)

    #execute request
    c.perform()
    c.close()

    #print response
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))


if __name__ == "__main__":
    main(sys.argv[1:])
