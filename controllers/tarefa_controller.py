from bottle import Bottle, request, template, redirect, BaseResponse
from .base_controller import BaseController
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService 
from datetime import datetime 
import json 

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
        
        self.app.route('/tarefas/toggle/<tarefa_id:int>', method='POST', callback=self.toggle_status)

        self.app.route('/tarefas/add', method='GET', callback=self.add_form)
        self.app.route('/tarefas/add', method='POST', callback=self.add)

        self.app.route('/tarefas/concluidas', method='GET', callback=self.concluidas)

    def _reconstruct_datetime(self, data_vencimento, hora_input):
        """Combina a data de vencimento com a hora (HH:MM) para criar o timestamp completo."""
        if not hora_input:
            return None
        
        base_date = data_vencimento if data_vencimento else datetime.now().strftime('%Y-%m-%d')
        
        return f"{base_date}T{hora_input}"

    def list_tpl(self):
        status_filtro = request.query.get('status', None) 
        sort_by = request.query.get('sort', 'id') 
        
        tarefas = self.service.get_filtered_and_sorted(status=status_filtro, sort_by=sort_by)

        return template("tarefa.tpl", 
                        tarefas=tarefas,
                        current_status=status_filtro,
                        current_sort=sort_by)

    def add_form(self):
        return template("tarefa_form.tpl") 

    def add(self):
        nome = request.forms.get('nome')
        descricao = request.forms.get('descricao')
        prioridade = request.forms.get('prioridade')
        data_vencimento = request.forms.get('data_vencimento') or None
        
        hora_inicio_input = request.forms.get('hora_inicio_input')
        hora_fim_input = request.forms.get('hora_fim_input')

        data_hora_inicio_full = self._reconstruct_datetime(data_vencimento, hora_inicio_input)
        data_hora_fim_full = self._reconstruct_datetime(data_vencimento, hora_fim_input)

        self.service.add( 
            nome=nome, 
            descricao=descricao, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio_full, 
            data_hora_fim=data_hora_fim_full      
        )
        return redirect('/tarefas') 

    def concluidas(self):
        tarefas = self.service.get_concluidas()
        return {"concluidas": [t.to_dict() for t in tarefas]}
    
    def delete(self, tarefa_id):
        self.service.delete(tarefa_id)
        return redirect('/tarefas')
    
    def edit_form(self, tarefa_id):
        tarefa = self.service.get_by_id(tarefa_id)
        return template("tarefa_form.tpl", tarefa=tarefa) 

    def edit(self, tarefa_id):
        nome = request.forms.get('nome')
        descricao = request.forms.get('descricao')
        prioridade = request.forms.get('prioridade')
        data_vencimento = request.forms.get('data_vencimento') or None

        hora_inicio_input = request.forms.get('hora_inicio_input')
        hora_fim_input = request.forms.get('hora_fim_input')
        
        data_hora_inicio_full = self._reconstruct_datetime(data_vencimento, hora_inicio_input)
        data_hora_fim_full = self._reconstruct_datetime(data_vencimento, hora_fim_input)

        self.service.update(
            tarefa_id=tarefa_id,
            nome=nome, 
            descricao=descricao, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio_full, 
            data_hora_fim=data_hora_fim_full      
        )
        return redirect('/tarefas')

    def toggle_status(self, tarefa_id):
        try:
            data = request.json
            new_status = bool(data.get('isConcluida'))
        except (TypeError, json.JSONDecodeError):
            return BaseResponse('Status de conclusão inválido ou ausente.', status=400)
            
        success = self.service.toggle_concluida(tarefa_id, new_status)

        if success:
            return {'status': 'success', 'id': tarefa_id, 'isConcluida': new_status}
        else:
            return BaseResponse('Tarefa não encontrada.', status=404)


tarefa_routes = Bottle()

def load_controller():
    return TarefaController(tarefa_routes)