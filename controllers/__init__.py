from bottle import Bottle
from .tarefa_controller import tarefa_routes
from .user_controller import user_routes
from .home_controller import home_routes
from .tarefa_controller import load_controller as load_tarefa
from .user_controller import load_controller as load_user
from .home_controller import load_controller as load_home
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService

def init_controllers(app: Bottle):
    print("🔄 Inicializando dependências...")
    tarefa_model = TarefaModel()
    tarefa_service = TarefaService(tarefa_model)

    print("🔄 Carregando controladores...")
   
    load_tarefa(tarefa_service) 
    load_user()
    load_home()
    app.merge(tarefa_routes)
    app.merge(user_routes)
    app.merge(home_routes)
    
    print("✅ Todas as rotas foram carregadas com sucesso!")