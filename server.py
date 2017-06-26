
from cgi import parse_qs
from urllib import quote
from wsgiref.simple_server import make_server
import time
import json
import requests


#
# "business" functions

def fetch_yahoo_tickers(tickers):

    t0 = time.time()

    tickers = \
      ','.join(map((lambda t: '"' + t + '"'), tickers.split(',')))
    query = \
      'select * from yahoo.finance.quotes where symbol in (' + tickers + ')'
    #print(query)
    uri = \
      'https://query.yahooapis.com/v1/public/yql' + \
      '?q=' + quote(query) + \
      '&format=json' + \
      '&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
    #print(uri)

    res = requests.get(uri)
    if res.status_code != 200: return res.status_code

    data = res.json()['query']

    quotes = data['results']['quote']
    if data['count'] < 2: quotes = [ quotes ]

    result = map(
      lambda q: dict( \
        symbol=q['Symbol'], \
        currency=q['Currency'], \
        price=float(q['LastTradePriceOnly'])),
      quotes)
    #print result
    print 'fetching ' + tickers + \
      ', found ' + str(data['count']) + ' quotes' + \
      ', took ' + str(time.time() - t0) + 's'

    return result

#
# route helpers

def respond(env, start, content_type, body, status='200 OK'):
    headers = [
      ('Content-Type', content_type),
      ('Content-Length', str(len(body))) ]
    start(status, headers)
    return [ body ]

#
# route implementations

def fourofour(env, start):
    return respond(env, start, 'text/plain', 'Four O Four', '404 Not Found.')

def quotes(env, start):

    params = parse_qs(env['QUERY_STRING'])
    tickers = params.get('tickers', [ '' ])[0]

    quotes = fetch_yahoo_tickers(tickers)

    body = 'window._quotes = window._quotes || {};\n'
    for q in quotes:
      body = body + \
        'window._quotes["' + str(q['symbol']) + '"] = ' + json.dumps(q) + ';\n'

    start('200 OK', [
      ('Content-Type', 'application/javascript'),
      ('Content-Length', str(len(body))),
      ('Cache-Control', 'max-age=300') ])
    return [ body ]

routes = {
  'quotes.js': quotes
}

#
# application

def application(environment, start_response):

    path0 = environment.get('PATH_INFO').split('/')[1]
    route = routes.get(path0, fourofour)

    return route(environment, start_response)

make_server('127.0.0.1', 8080, application).serve_forever()

