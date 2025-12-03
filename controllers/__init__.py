from bottle import Bottle

# Importa as rotas e as funções de carga (factories) dos controladores
from .tarefa_controller import tarefa_routes, load_controller as load_tarefa
from .user_controller import user_routes, load_controller as load_user
from .home_controller import home_routes, load_controller as load_home

# Importa o Serviço de Tarefas para Injeção de Dependência
# Necessário porque o TarefaController no seu código espera receber 'tarefa_service' no __init__
try:
    from services.tarefa_service import TarefaService
except ImportError:
    print("⚠️  AVISO: 'services/tarefa_service.py' não encontrado.")
    TarefaService = None

def init_controllers(app: Bottle):
    """
    Inicializa dependências, carrega controladores e funde rotas na app principal.
    """
    
    # 1. Inicializar Tarefas (Passando o Service)
    if TarefaService:
        print("🔧 Inicializando Serviço de Tarefas...")
        # Cria a instância do serviço aqui
        tarefa_service = TarefaService()
        # Passa a instância para a função load_controller do tarefa_controller.py
        load_tarefa(tarefa_service) 
    else:
        print("❌ ERRO: Não foi possível carregar o TarefaController (Service ausente).")

    # 2. Inicializar User e Home
    # (Baseado no seu código anterior, estes não exigem argumentos no load)
    load_user()
    load_home()
    
    # 3. Fundir as rotas (Merge) na aplicação principal
    # Isto conecta as rotas definidas nos ficheiros individuais ao servidor principal
    app.merge(user_routes)
    app.merge(tarefa_routes)  
    app.merge(home_routes)
    
    print("✅ Todas as rotas foram carregadas com sucesso!")