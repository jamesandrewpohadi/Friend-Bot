# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
from skills import *

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = filterRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    
    return r
    #return request.args['hub.challenge']

def filterRequest(req):
    if req.get("result").get("action") == "yahooWeatherForecast":
        r = processRequestWeatherApixu(req)
    elif req.get("result").get("action") == "exchangeRate":
        r = processRequestExchangeRate(req)
    elif req.get("result").get("action") == "checkPrime":
        r = processP_Check(req)
    elif req.get("result").get("action") == "askMod":
        r = mod(req)
    elif req.get("result").get("action") == "askEuler":
        r = euler(req)
    else:
        r={}
    return r



def processRequestExchangeRate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    from_ = parameters.get("From")
    to = parameters.get("To")
    datar = urlopen("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=" + from_ + "&to_currency=" + to + "&apikey=6ORVWXEP5FRY0SZ7").read()
    data = json.loads(datar)
    res = makeWebhookResultExchange(data)
    return res

def processRequestWeather(req):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processRequestWeatherApixu(req):
    city = req.get("result").get("parameters").get("geo-city")
    datas = urlopen("http://api.apixu.com/v1/current.json?key=b9a7898e06294d5d99603603172711&q=" + city ).read()
    data = json.loads(datas)
    res = makeWebhookResultWeatherApixu(data)
    return res

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def makeWebhookResultExchange(data):
    Realtime = data.get("Realtime Currency Exchange Rate")
    Exchange_Rate = Realtime.get("5. Exchange Rate")
    from_ = Realtime.get("1. From_Currency Code")
    to = Realtime.get("3. To_Currency Code")
    return {
        "speech": "The exchange rate (" + from_ + " to " + to + ") is " + Exchange_Rate,
        "displayText": "The exchange rate is " + Exchange_Rate,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResultWeatherApixu(data):
    city = data.get('location').get('name')
    condition = data.get('current').get('condition').get('text')
    temperature = data.get('current').get('temp_c')
    feelslike_c = data.get('current').get('feelslike_c')
    return {
        "speech": "The current weather in " + city + " is " + condition + " and the temperature is " + str(temperature) + " C (feels like " + str(feelslike_c) + " C)",
        "displayText": "The current weather in " + city + " is " + condition + " and the temperature is " + str(temperature) + " C (feels like " + str(feelslike_c) + " C)",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + " is " + condition.get('text') + \
             ", and the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
