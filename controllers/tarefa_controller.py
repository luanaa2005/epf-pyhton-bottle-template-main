from bottle import Bottle, request, template, redirect
from .base_controller import BaseController
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService

class TarefaController(BaseController):
    def __init__(self, app):
        super().__init__(app)

        model = TarefaModel()
        self.service = TarefaService(model)

        self.setup_routes()

    def setup_routes(self):
        self.app.route('/tarefas', method='GET', callback=self.list_tpl)
        self.app.route('/tarefas/delete/<tarefa_id:int>', method=['GET','POST'], callback=self.delete)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='GET', callback=self.edit_form)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='POST', callback=self.edit)

        self.app.route('/tarefas/add', method='GET', callback=self.add_form)
        self.app.route('/tarefas/add', method='POST', callback=self.add)

        self.app.route('/tarefas/concluidas', method='GET', callback=self.concluidas)

    def list_tpl(self):
        tarefas = self.service.get_all()
        return template("tarefa.tpl", tarefas=tarefas)

    def add_form(self):
        return template("tarefa_add.tpl")  

    def add(self):
        self.service.save()
        return redirect('/tarefas')  

    def concluidas(self):
        tarefas = self.service.get_concluidas()
        return {"concluidas": [t.to_dict() for t in tarefas]}
    
    def delete(self, tarefa_id):
        self.service.delete(tarefa_id)
        return redirect('/tarefas')
    
    def edit_form(self, tarefa_id):
        tarefa = self.service.get_by_id(tarefa_id)
        return template("tarefa_edit.tpl", tarefa=tarefa)

    def edit(self, tarefa_id):
        self.service.update(tarefa_id)
        return redirect('/tarefas')



tarefa_routes = Bottle()

def load_controller():
    return TarefaController(tarefa_routes)