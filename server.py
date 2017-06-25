
from wsgiref.simple_server import make_server

#
# route implementations

def hello(env, start):
    res_body = "Hello."
    res_status = "200 OK"
    res_headers = [ ("Content-Length", str(len(res_body))) ]
    start(res_status, res_headers)
    return [ res_body ]

def quotes(env, start):
    res_body = "QUOTES!"
    res_status = "200 OK"
    res_headers = [ ("Content-Length", str(len(res_body))) ]
    start(res_status, res_headers)
    return [ res_body ]

#
# application

def application(environment, start_response):
    path0 = environment.get('PATH_INFO').split('/')[1]
    route = {
      "quotes.js": quotes
    }.get(path0, hello)
    return route(environment, start_response)

make_server('127.0.0.1', 8080, application).serve_forever()

