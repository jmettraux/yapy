
from wsgiref.simple_server import make_server

def application(environment, start_response):
    #path = environment.get('PATH_INFO')
    res_body = "Hello."
    res_status = "200 OK"
    res_headers = [ ("Content-Length", str(len(res_body))) ]
    start_response(res_status, res_headers)
    return [ res_body ]

make_server('127.0.0.1', 8080, application).serve_forever()

