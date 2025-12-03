from bottle import Bottle, BaseRequest, static_file, route, template
import bottle 
from config import Config
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService
from controllers.tarefa_controller import load_controller as load_tarefa_controller
from controllers.user_controller import load_controller as load_user_controller
import os

BaseRequest.default_content_type = 'application/x-www-form-urlencoded; charset=UTF-8'

class App:
    def __init__(self):
        self.bottle = Bottle()
        self.bottle.default_response_encoding = 'utf-8'
        self.config = Config()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        VIEWS_PATH = os.path.join(BASE_DIR, 'views')
        if VIEWS_PATH not in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.insert(0, VIEWS_PATH)

        self.tarefa_model = TarefaModel()
        self.tarefa_service = TarefaService(self.tarefa_model)
        self.bottle.tarefa_service = self.tarefa_service

    def setup_routes(self):
        print('🚀 Inicializa rotas!')
        @self.bottle.route('/')
        def serve_home():
            return template('home')

        @self.bottle.route('/login')
        def serve_login():
            return template('login', error=None)

        @self.bottle.route('/tarefas-app')
        def serve_tarefas_app():
            return template('index')
            
        @self.bottle.route('/static/<filepath:path>')
        def serve_static(filepath):
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            STATIC_PATH = os.path.join(BASE_DIR, 'static')
            return static_file(filepath, root=STATIC_PATH)
        tarefa_controller_instance = load_tarefa_controller(self.tarefa_service) 
        self.bottle.merge(tarefa_controller_instance.app)
        user_controller_instance = load_user_controller()
        self.bottle.merge(user_controller_instance.app)

    def run(self):
        self.setup_routes()
        self.bottle.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG,
            reloader=self.config.RELOADER
        )

def create_app():
    return App()