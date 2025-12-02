from bottle import Bottle, request, template, redirect, BaseResponse
from .base_controller import BaseController
from datetime import datetime 
import json 

class TarefaController(BaseController):
    def __init__(self, app, tarefa_service): 
        super().__init__(app)
        self.service = tarefa_service 

        self.setup_routes()

    def setup_routes(self):
        self.app.route('/tarefas', method='GET', callback=self.api_list) 
        self.app.route('/tarefas/add', method='POST', callback=self.api_add)
        self.app.route('/tarefas/toggle/<tarefa_id:int>', method='POST', callback=self.toggle_status)
        self.app.route('/tarefas/delete/<tarefa_id:int>', method=['GET','POST'], callback=self.delete)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='GET', callback=self.edit_form)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='POST', callback=self.edit)
        self.app.route('/tarefas/agenda', method='GET', callback=self.calendar_view)

    def api_list(self):
        status_filtro = request.query.get('status', None) 
        sort_by = request.query.get('sort', 'id') 
        
        tarefas = self.service.get_filtered_and_sorted(status=status_filtro, sort_by=sort_by)
        tarefas_json = [t.to_dict() for t in tarefas]

        return {"tarefas": tarefas_json}

    def api_add(self):
        nome = request.forms.get('nome')
        prioridade = request.forms.get('prioridade')
        if not nome or not prioridade:
             return BaseResponse('Nome e Prioridade são obrigatórios.', status=400)

        descricao = request.forms.get('descricao')
        data_vencimento = request.forms.get('data_vencimento') or None
        data_hora_inicio = request.forms.get('data_hora_inicio') or None
        data_hora_fim = request.forms.get('data_hora_fim') or None

        tarefa_criada = self.service.add( 
            nome=nome, 
            descricao=descricao, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio, 
            data_hora_fim=data_hora_fim 
        )
        return tarefa_criada.to_dict()

    def delete(self, tarefa_id):
        self.service.delete(tarefa_id)
        return redirect('/tarefas')
    
    def edit_form(self, tarefa_id):
        tarefa = self.service.get_by_id(tarefa_id)
        return template("tarefa_form.tpl", tarefa=tarefa) 

    def edit(self, tarefa_id):
        self.service.update(
            tarefa_id=tarefa_id,
            nome=request.forms.get('nome'),
            descricao=request.forms.get('descricao'),
            prioridade=request.forms.get('prioridade'),
            data_vencimento=request.forms.get('data_vencimento') or None,
        )
        return redirect('/tarefas')

    def toggle_status(self, tarefa_id):
        try:
            data = request.json
            new_status = bool(data.get('isConcluida'))
        except (TypeError, AttributeError, json.JSONDecodeError):
            return BaseResponse('Inválido', status=400)
            
        success = self.service.toggle_concluida(tarefa_id, new_status)
        if success:
            return {'status': 'success', 'id': tarefa_id, 'isConcluida': new_status}
        return BaseResponse('Tarefa não encontrada.', status=404)

    def calendar_view(self):
        tarefas_agrupadas = self.service.get_tarefas_agrupadas_por_dia()
        return template('tarefa_calendar', title='Agenda', tarefas_agrupadas=tarefas_agrupadas)

tarefa_routes = Bottle()

def load_controller(tarefa_service):
    return TarefaController(tarefa_routes, tarefa_service)