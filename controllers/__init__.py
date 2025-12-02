from controllers.tarefa_controller import tarefa_routes
from controllers.user_controller import user_routes
from controllers.home_controller import home_routes
from bottle import Bottle
from .tarefa_controller import load_controller as load_tarefa
from .user_controller import load_controller as load_user
from .home_controller import load_controller as load_home

def init_controllers(app: Bottle):
    load_tarefa()
    load_user()
    load_home()
    
    app.merge(user_routes)
    app.merge(tarefa_routes)  
    app.merge(home_routes)

