from bottle import Bottle, BaseRequest, static_file, route, template
import bottle # Importante para configurar o TEMPLATE_PATH
from config import Config
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService
# 🟢 ALTERAÇÃO: Importamos ambos os controllers com alias para evitar conflito de nomes
from controllers.tarefa_controller import load_controller as load_tarefa_controller
from controllers.user_controller import load_controller as load_user_controller
import os

# Define o Content-Type padrão
BaseRequest.default_content_type = 'application/x-www-form-urlencoded; charset=UTF-8'

class App:
    def __init__(self):
        self.bottle = Bottle()
        self.bottle.default_response_encoding = 'utf-8'
        self.config = Config()

        # Configuração do Caminho dos Templates (Views)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        VIEWS_PATH = os.path.join(BASE_DIR, 'views')
        if VIEWS_PATH not in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.insert(0, VIEWS_PATH)

        # Inicialização do Service e Model
        self.tarefa_model = TarefaModel()
        self.tarefa_service = TarefaService(self.tarefa_model)
        self.bottle.tarefa_service = self.tarefa_service

    def setup_routes(self):
        print('🚀 Inicializa rotas!')
        
        # --- 1. ROTAS DE PÁGINAS (Usando template .tpl) ---
        
        # Rota Raiz: Menu Inicial
        @self.bottle.route('/')
        def serve_home():
            # Renderiza views/home.tpl
            return template('home')

        # Rota de Login (Separada)
        @self.bottle.route('/login')
        def serve_login():
            # Renderiza views/login.tpl
            return template('login', error=None)

        # Rota da App Principal (Tarefas)
        @self.bottle.route('/tarefas-app')
        def serve_tarefas_app():
            # Renderiza views/index.tpl
            return template('index')
            
        # --- 2. ROTA DE ARQUIVOS ESTÁTICOS (CSS, JS, IMG) ---
        @self.bottle.route('/static/<filepath:path>')
        def serve_static(filepath):
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            STATIC_PATH = os.path.join(BASE_DIR, 'static')
            return static_file(filepath, root=STATIC_PATH)
        
        # --- 3. MONTAGEM DOS CONTROLLERS ---
        
        # A) TAREFAS
        # Carrega o controller injetando o serviço
        tarefa_controller_instance = load_tarefa_controller(self.tarefa_service) 
        
        # 🟢 CORREÇÃO: Usar 'merge' em vez de 'mount'
        # Isso remove o prefixo '/api', permitindo acessar '/tarefas' diretamente
        self.bottle.merge(tarefa_controller_instance.app)

        # B) USUÁRIOS (Páginas/Sistema)
        # Carrega o controller de usuários
        user_controller_instance = load_user_controller()
        # Fundimos (merge) na raiz porque as rotas já são '/users', '/users/add', etc.
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