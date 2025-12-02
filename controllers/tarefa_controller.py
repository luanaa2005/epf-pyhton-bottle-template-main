from bottle import Bottle, request, template, redirect, BaseResponse, route, view
from .base_controller import BaseController
from models.tarefa import TarefaModel
from services.tarefa_service import TarefaService 
from datetime import datetime 
import json 

class TarefaController(BaseController):
    # 🟢 CORREÇÃO 1: Aceita o TarefaService como argumento (Injeção de Dependência)
    def __init__(self, app, tarefa_service): 
        super().__init__(app)

        self.service = tarefa_service # Usa o service que foi passado

        self.setup_routes()

    def setup_routes(self):
        # ---------------------------------------------
        # ROTAS DE API RESTful (JSON) - CONSUMIDAS PELO FRONTEND SPA
        # Acessadas via /api/tarefas, /api/tarefas/add, etc.
        # ---------------------------------------------
        
        # Rota de Listagem (GET /api/tarefas)
        self.app.route('/tarefas', method='GET', callback=self.api_list) 
        
        # Rota de Adição (POST /api/tarefas/add)
        self.app.route('/tarefas/add', method='POST', callback=self.api_add)

        # Rota de Toggle Status (POST /api/tarefas/toggle/<tarefa_id>)
        self.app.route('/tarefas/toggle/<tarefa_id:int>', method='POST', callback=self.toggle_status)
        
        # ---------------------------------------------
        # ROTAS DE TEMPLATE (Legado)
        # ---------------------------------------------
        
        # Rotas TPL são mantidas separadas se você ainda as utiliza (Ex: Edição, Agenda)
        self.app.route('/tarefas/delete/<tarefa_id:int>', method=['GET','POST'], callback=self.delete)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='GET', callback=self.edit_form)
        self.app.route('/tarefas/edit/<tarefa_id:int>', method='POST', callback=self.edit)
        self.app.route('/tarefas/agenda', method='GET', callback=self.calendar_view)
        # Rota TPL de listagem foi removida ou renomeada para evitar conflito com a API GET /tarefas

    
    # ---------------------------------------------
    # MÉTODOS DE API (JSON)
    # ---------------------------------------------
    
    def api_list(self):
        """Retorna a lista de tarefas filtrada e ordenada em formato JSON."""
        status_filtro = request.query.get('status', None) 
        sort_by = request.query.get('sort', 'id') 
        
        tarefas = self.service.get_filtered_and_sorted(status=status_filtro, sort_by=sort_by)

        # Assume que o método to_dict() existe no Model Tarefa
        tarefas_json = [t.to_dict() for t in tarefas]

        return {"tarefas": tarefas_json}

    def api_add(self):
        """Adiciona uma nova tarefa a partir de dados de formulário e retorna a tarefa criada em JSON."""
        nome = request.forms.get('nome')
        descricao = request.forms.get('descricao')
        prioridade = request.forms.get('prioridade')
        
        data_vencimento = request.forms.get('data_vencimento') or None
        data_hora_inicio_full = request.forms.get('data_hora_inicio') or None
        data_hora_fim_full = request.forms.get('data_hora_fim') or None

        if not nome or not prioridade:
            return BaseResponse('Nome e Prioridade são obrigatórios.', status=400)

        tarefa_criada = self.service.add( 
            nome=nome, 
            descricao=descricao, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio_full, 
            data_hora_fim=data_hora_fim_full 
        )
        return tarefa_criada.to_dict()
    
    # ---------------------------------------------
    # MÉTODOS EXISTENTES (Mantidos para a funcionalidade completa)
    # ---------------------------------------------
    
    # ... (Os métodos list_tpl, add_form, add, concluidas, delete, edit_form, edit, toggle_status e calendar_view 
    # permanecem inalterados, mas não são mais usados pelo Frontend SPA para listagem/adição principal) ...

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
        response = redirect('/tarefas')
        response.content_type = 'text/html; charset=utf-8'
        return response

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
        
        response = redirect('/tarefas')
        response.content_type = 'text/html; charset=utf-8'
        return response

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

    @route('/tarefas/agenda')
    @view('tarefa_calendar')
    def calendar_view(self):
        tarefas_agrupadas = self.service.get_tarefas_agrupadas_por_dia()
        
        return{
            'title': 'Agenda de Tarefas',
            'tarefas_agrupadas': tarefas_agrupadas
        }

# Objeto Bottle secundário para montar as rotas do Controller
tarefa_routes = Bottle()

# 🟢 CORREÇÃO 2: Aceita e passa o service para a classe
def load_controller(tarefa_service):
    return TarefaController(tarefa_routes, tarefa_service)