from bottle import Bottle,template
from .base_controller import BaseController

class HomeController(BaseController):
    def __init__(self,app):
        super().__init__(app)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route('/', method='GET', callback=self.index)

    def index(self):
        return template('home')
    
home_routes = Bottle()

def load_controller():
    return HomeController(home_routes)