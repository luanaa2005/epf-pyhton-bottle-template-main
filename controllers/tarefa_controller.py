from bottle import Bottle, request, template, redirect, BaseResponse, route, view
from .base_controller import BaseController
from services.tarefa_service import TarefaService 
from datetime import datetime 
import json 

class TarefaController(BaseController):
    def __init__(self, app, tarefa_service): 
        super().__init__(app)
        self.service = tarefa_service
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/tarefas', method='GET', callback=self.list_tpl) 
        self.app.route('/tarefas/add', method='POST', callback=self.add) 
        self.app.route('/tarefas/add', method='GET', callback=self.add_form) 
        self.app.route('/tarefas/delete/<tarefa_id:int>', method=['POST'], callback=self.delete)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='GET', callback=self.edit_form)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='POST', callback=self.edit)
        self.app.route('/tarefas/toggle/<tarefa_id:int>', method='POST', callback=self.toggle_status)
        self.app.route('/tarefas/agenda', method='GET', callback=self.calendar_view)
        self.app.route('/api/tarefas', method='GET', callback=self.api_list)



    def list_tpl(self):
        """Renderiza a página HTML com a lista de tarefas"""
        status_filtro = request.query.get('status', None) 
        sort_by = request.query.get('sort', 'id') 
        

        tarefas = self.service.get_filtered_and_sorted(status=status_filtro, sort_by=sort_by)
  
        return template("tarefa", 
                        tarefas=tarefas, 
                        current_status=status_filtro, 
                        current_sort=sort_by)

    def add_form(self):
        return template("tarefa_form") 

    def edit_form(self, tarefa_id):
        tarefa = self.service.get_by_id(tarefa_id)
        return template("tarefa_form", tarefa=tarefa) 

    def calendar_view(self):
        tarefas_agrupadas = self.service.get_tarefas_agrupadas_por_dia()
        return template('tarefa_calendar', title='Agenda de Tarefas', tarefas_agrupadas=tarefas_agrupadas)


    def add(self):
        """Recebe o formulário HTML e salva"""
        nome = request.forms.get('nome')
        descricao = request.forms.get('descricao')
        prioridade = request.forms.get('prioridade')
        
        data_vencimento = request.forms.get('data_vencimento') or None
        

        hora_inicio = request.forms.get('hora_inicio_input')
        hora_fim = request.forms.get('hora_fim_input')

        data_hora_inicio = self._reconstruct_datetime(data_vencimento, hora_inicio)
        data_hora_fim = self._reconstruct_datetime(data_vencimento, hora_fim)

        self.service.add( 
            nome=nome, 
            descricao=descricao, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio, 
            data_hora_fim=data_hora_fim 
        )
        return redirect('/tarefas') 

    def edit(self, tarefa_id):
        nome = request.forms.get('nome')
        descricao = request.forms.get('descricao')
        prioridade = request.forms.get('prioridade')
        data_vencimento = request.forms.get('data_vencimento') or None
        
        hora_inicio = request.forms.get('hora_inicio_input')
        hora_fim = request.forms.get('hora_fim_input')

        dt_inicio = request.forms.get('data_hora_inicio') 
        if not dt_inicio and hora_inicio:
            dt_inicio = self._reconstruct_datetime(data_vencimento, hora_inicio)

        dt_fim = request.forms.get('data_hora_fim')
        if not dt_fim and hora_fim:
            dt_fim = self._reconstruct_datetime(data_vencimento, hora_fim)

        self.service.update(
            tarefa_id=tarefa_id,
            nome=nome, descricao=descricao, prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=dt_inicio, 
            data_hora_fim=dt_fim       
        )
        return redirect('/tarefas')

    def delete(self, tarefa_id):
        self.service.delete(tarefa_id)
        return redirect('/tarefas')

    def toggle_status(self, tarefa_id):
        try:
            if request.json:
                new_status = bool(request.json.get('isConcluida'))
            else:
                return BaseResponse('Formato inválido', 400)
                
            self.service.toggle_concluida(tarefa_id, new_status)
            return {'status': 'success'}
        except Exception as e:
            print(f"Erro no toggle: {e}")
            return BaseResponse('Erro no servidor', 500)

    
    def api_list(self):
        """Retorna JSON (Usado apenas pela rota /api/tarefas se necessário)"""
        status_filtro = request.query.get('status', None) 
        sort_by = request.query.get('sort', 'id') 
        tarefas = self.service.get_filtered_and_sorted(status=status_filtro, sort_by=sort_by)
        return {"tarefas": [t.to_dict() for t in tarefas]}

    def _reconstruct_datetime(self, data_vencimento, hora_input):
        if not hora_input: return None
        base_date = data_vencimento if data_vencimento else datetime.now().strftime('%Y-%m-%d')
        if len(hora_input) > 5: hora_input = hora_input[:5]
        return f"{base_date}T{hora_input}"

tarefa_routes = Bottle()

def load_controller(tarefa_service):
    return TarefaController(tarefa_routes, tarefa_service)