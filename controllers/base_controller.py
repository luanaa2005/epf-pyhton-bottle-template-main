from bottle import redirect, HTTPResponse, template

class BaseController:
    def __init__(self, app):
        self.app = app
        
    def render(self, filename, **context):
        return template(filename, **context)
    
    def redirect(self, path, code=302):
        try:
            return redirect(path, code)
        except Exception:
            res = HTTPResponse(status=code)
            res.set_header('Location', path)
            return res