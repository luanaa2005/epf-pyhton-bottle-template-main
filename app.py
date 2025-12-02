from bottle import Bottle, BaseRequest 
from config import Config
from models.tarefa import TarefaModel, Tarefa
from services.tarefa_service import TarefaService


BaseRequest.default_content_type = 'application/x-www-form-urlencoded; charset=UTF-8'

class App:
    def __init__(self):
        self.bottle = Bottle()
        self.config = Config()

        self.tarefa_model = TarefaModel()
        self.tarefa_service = TarefaService(self.tarefa_model)

    def setup_routes(self):
        from controllers import init_controllers
        print('🚀 Inicializa rotas!')
        init_controllers(self.bottle)

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