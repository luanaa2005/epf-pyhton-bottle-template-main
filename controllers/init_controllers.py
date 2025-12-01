from .tarefa_controller import tarefa_routes

def init_controllers(app: Bottle):
    app.merge(tarefa_routes)
    print("✅ Rotas de tarefas inicializadas!")
