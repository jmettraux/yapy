
from cgi import parse_qs
from wsgiref.simple_server import make_server


#
# route helpers

def respond(env, start, content_type, body):
    status = '200 OK'
    headers = [
      ('Content-Type', content_type),
      ('Content-Length', str(len(body))) ]
    start(status, headers)
    return [ body ]

#
# route implementations

def hello(env, start):
    return respond(env, start, 'text/plain', 'Hello.')

def quotes(env, start):
    params = parse_qs(env['QUERY_STRING'])
    tickers = params.get('tickers', [ '' ])[0].split(',')
    body = 'quotes for ' + ', '.join(tickers)
    return respond(env, start, 'text/plain', body)

routes = {
  'quotes.js': quotes
}

#
# application

def application(environment, start_response):
    path0 = environment.get('PATH_INFO').split('/')[1]
    route = routes.get(path0, hello)
    return route(environment, start_response)

make_server('127.0.0.1', 8080, application).serve_forever()

