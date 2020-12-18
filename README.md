# Pelion Device Management Python Webhook Example

This is a simple example using python packages pycurl a webhook notification channel with Pelion Device Management

This allows you to subscribe to resources and get notifications if they change.

Created by Mac Lobdell

## Setup

Install Python 3 (I tested this with Python 3.7.6), then run the following commands.

```
pip install pycurl
```

## Usage

Connect a device to Pelion Device Management and get an API key. Follow the guide at https://www.pelion.com/guides/connect-device-to-pelion/.

Follow the guide to setup API Gateway, Lambda, and Elasticsearch on AWS at https://github.com/PelionIoT/pelion-aws-lambda-webhook-example. This example replaces the CURL commands referenced in the guide. 

Use this script instead of the CURL commands referenced there. 


To run the script:

`python pelion_webhook.py <API_KEY> <AWS_API_KEY> <AWS WEBHOOK CALLBACK URL>`

Example:

`python pelion_webhook.py ak_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx yyyyyyyyyyyyyyyyyyyyyyyy abcabcabcabc.execute-api.us-west-2.amazonaws.com/default/pass_pelion_data`