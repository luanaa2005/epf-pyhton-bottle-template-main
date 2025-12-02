from bottle import Bottle
from bottle import Bottle, static_file
from config import Config
from models.tarefa import TarefaModel, Tarefa
from services.tarefa_service import TarefaService

class App:
    def __init__(self):
        self.bottle = Bottle()
        self.config = Config()

        self.tarefa_model = TarefaModel()
        self.tarefa_service = TarefaService(self.tarefa_model)

        self.tarefa_model.add_tarefa(Tarefa(1, "Estudar Python", "Revisar Bottle e Flask", False, "Alta"))
        self.tarefa_model.add_tarefa(Tarefa(2, "Fazer exercícios", "Resolver listas de lógica", True, "Média"))
        self.tarefa_model.add_tarefa(Tarefa(3, "Ler artigos", "Ler sobre APIs REST", False, "Baixa"))

    def setup_routes(self):
        from controllers import init_controllers
        print('🚀 Inicializa rotas!')
        init_controllers(self.bottle)

        @self.bottle.route('/static/<filepath:path>')
        def server_static(filepath):
            return static_file(filepath, root='./static')
    
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
