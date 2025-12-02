from controllers.tarefa_controller import tarefa_routes
from controllers.user_controller import user_routes
from bottle import Bottle, redirect
from .tarefa_controller import load_controller

def init_controllers(app: Bottle):
    load_controller()
    app.merge(user_routes)
    app.merge(tarefa_routes)  

    @app.route('/')
    def index():
        return redirect('/tarefas')
