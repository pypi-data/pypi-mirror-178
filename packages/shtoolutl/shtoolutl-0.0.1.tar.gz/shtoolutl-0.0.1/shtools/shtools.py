import os
import socket
import requests
import urllib.request
import http.client
import time
import ssl

############################TEST##############################
def SHtest():
    return True 
    
httpcode = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }
# Fonction récupe les infos basique d'un site web
def infoweb(webstr, obj):
    """
    Enter a domain and obj --> <infoweb('<website>','<obj>')>
    obj List: 
     -all: pulls out a dictionary of all the information on the website
     -domain
     -ip
     -code
     -statut
     -statut-code
    """
    #Gestion des entrés
    assert type(webstr) == str
    assert obj != '' 
    #Variable le disctionnaire
    disctList = None
    


    #Requête WEB
    domain = webstr.replace('https://', '')
    webip= socket.gethostbyname(domain)
    webtest = 0
    r = requests.get(f'{webstr}', auth=('user', 'pass'))
    webcode = r.status_code
    webcheck = httpcodeinfo(r.status_code)
    Httpinfo = r.text
    #Disctionnaire des informations du WEB
    dictwebinfo = {"domain":domain,"ip": webip, "code": webcode,"statut":webcheck[1],"statu-info":webcheck[1]}
    #Gestion de la valeur 'obj'
    
    if obj == 'all':
      disctList = dictwebinfo 
    else:
      disctList = dictwebinfo[obj]
            

    return disctList
# Fonction pour avoir des infos sur le code de requete spécial
def httpcodeinfo(code):
      """
      Enter: <http code>
      Return: ('<statut>','<Description>')
      """
      assert type(code) == int
      return httpcode[code]


#Test fonction
print(infoweb('https://google.com','ip'))