__version__ = "0.0.0.1"
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
from configparser import ConfigParser
from os.path import expanduser, isdir
from markdown import markdown

def md(s):
    return '<html><head><meta charset="utf-8"/></head><body>\n'+markdown(s)+'\n</body></html>'

defaulterr = """
# Error 404

I'm sorry :-(

File not found.
"""

def configure():
    cfg = ConfigParser()
    cfg.read(expanduser("~")+"/.config/muzne.cfg")
    return {'port':int(cfg['Setup']['Port']) if 'Port' in cfg['Setup'] else 8080,
    'dir':cfg['Setup']['Dir'],
    '404':cfg['Setup']['404'] if '404' in cfg['Setup'] else ''}

class html(BaseHTTPRequestHandler):
    def do_GET(self):
        cfg = configure()
        pathy = self.path
        pathy = unquote_plus(pathy)
        if isdir(pathy):
            pathy = pathy + 'index.md'
        print(pathy)
        diry = cfg['dir']
        try:
            code = 200
            message = md(open(f'{diry}/{pathy}').read())
        except:
            code = 404
            errpg = cfg['404']
            try:
                message = md(open(f'{diry}/{errpg}').read())
            except FileNotFoundError:
                message = md(defaulterr)
            except KeyError:
                message = markdown(defaulterr)
            except PermissionError:
                message = md(defaulterr)
        self.send_response(code)
        self.send_header('Content-type','text/html;charset=utf-8')
        self.send_header('Content-Length',str(len(message)))
        
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        
def start():
    with HTTPServer(('', configure()['port']), html) as server:
        server.serve_forever()

if __name__ == "__main__":
    start()
