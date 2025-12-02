from bottle import Bottle, BaseRequest, static_file, route
from config import Config
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService
# Importa a função de carregar o Controller (agora configurada para receber o service)
from controllers.tarefa_controller import load_controller 
import os # 🟢 IMPORTAÇÃO NECESSÁRIA PARA O CAMINHO ABSOLUTO ROBUSTO

# Define o Content-Type padrão
BaseRequest.default_content_type = 'application/x-www-form-urlencoded; charset=UTF-8'

class App:
    def __init__(self):
        self.bottle = Bottle()
        
        self.bottle.default_response_encoding = 'utf-8'
        
        self.config = Config()

        self.tarefa_model = TarefaModel()
        self.tarefa_service = TarefaService(self.tarefa_model)
        
        # O self.bottle.tarefa_service não é mais estritamente necessário, 
        # mas pode ser útil para debug ou outros controllers.
        self.bottle.tarefa_service = self.tarefa_service

    def setup_routes(self):
        print('🚀 Inicializa rotas!')
        
        # --- 1. ROTAS DE ARQUIVOS ESTÁTICOS (HTML, CSS, JS) ---
        
        # Define o caminho absoluto para a pasta 'static' para rotas de HTML
        # Isso garante que os HTMLs (index.html, login.html) sejam encontrados
        STATIC_ROOT_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        
        # Rota para servir a página principal da aplicação (index.html)
        @self.bottle.route('/tarefas-app')
        def serve_tarefas_app():
            return static_file('index.html', root=STATIC_ROOT_HTML) 

        # Rota para servir o login
        @self.bottle.route('/')
        def serve_login():
            return static_file('login.html', root=STATIC_ROOT_HTML) 
            
        # Rota para servir arquivos estáticos gerais (CSS, JS, Imagens)
        @self.bottle.route('/static/<filepath:path>')
        def serve_static(filepath):
            # 🟢 CORREÇÃO FINAL ROBUSTA: Calcula o caminho absoluto
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            STATIC_PATH = os.path.join(BASE_DIR, 'static')
            return static_file(filepath, root=STATIC_PATH)
        
        # --- 2. MONTAGEM DO CONTROLLER (API) ---
        
        # 🟢 Passa explicitamente o TarefaService para load_controller
        tarefa_controller_instance = load_controller(self.tarefa_service) 
        
        # Monta as rotas do Controller sob o prefixo '/api'
        self.bottle.mount('/api', tarefa_controller_instance.app)


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

# if __name__ == '__main__':
#     app_instance = create_app()
#     app_instance.run()