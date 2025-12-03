import uuid
from datetime import datetime, date 
from models.tarefa import Tarefa 

class TarefaService:
    def __init__(self, model):
        self.model = model

    def _calculate_duration_hours(self, start_dt_str, end_dt_str):
        """Calcula a diferença em horas entre duas strings de data/hora."""
        if not start_dt_str or not end_dt_str:
            return None
        try:
            start_dt = datetime.strptime(start_dt_str, '%Y-%m-%dT%H:%M')
            end_dt = datetime.strptime(end_dt_str, '%Y-%m-%dT%H:%M')
            
            duration = end_dt - start_dt
            
            total_hours = duration.total_seconds() / 3600
            
            return round(total_hours, 2)
            
        except ValueError:
            return None 

    def get_tarefas(self):
        return self.model.get_all()

    def get_by_id(self, tarefa_id):
        return self.model.get_by_id(tarefa_id)
    
    def get_filtered_and_sorted(self, status=None, sort_by='id'):
        """
        Retorna tarefas filtradas e ordenadas, adicionando o atributo de duração.
        """
        tarefas = self.model.get_filtered_and_sorted(status, sort_by)
        
        for t in tarefas:
            duration = self._calculate_duration_hours(t.data_hora_inicio, t.data_hora_fim)
            setattr(t, 'duration_hours', duration) 
            
        return tarefas
    
    
    def get_tarefas_agrupadas_por_dia(self):
        
        tarefas = self.get_tarefas() 
    
        tarefas_por_dia = {}

        for tarefa in tarefas:
            data_vencimento_str = tarefa.data_vencimento
            if data_vencimento_str:
                try:
                    data_obj = datetime.strptime(data_vencimento_str, "%Y-%m-%d").date()

                    chave_dia = data_obj
                    
                    if chave_dia not in tarefas_por_dia:
                        tarefas_por_dia[chave_dia] = []
                    duration = self._calculate_duration_hours(tarefa.data_hora_inicio, tarefa.data_hora_fim)
                    setattr(tarefa, 'duration_hours', duration)
                    
                    tarefas_por_dia[chave_dia].append(tarefa)
                
                except ValueError:
                    continue
            
        
        return tarefas_por_dia

    
    def add(self, nome, descricao, prioridade, data_vencimento, data_hora_inicio, data_hora_fim):
        novo_id = self._generate_unique_id()
        tarefa = Tarefa(
            id=novo_id, 
            nome=nome, 
            descricao=descricao, 
            isConcluida=False, 
            prioridade=prioridade, 
            data_vencimento=data_vencimento,
            data_hora_inicio=data_hora_inicio,
            data_hora_fim=data_hora_fim
        )
        self.model.add_tarefa(tarefa)
        return tarefa

    def update(self, tarefa_id, nome, descricao, prioridade, data_vencimento, data_hora_inicio, data_hora_fim):
        tarefa = self.model.get_by_id(tarefa_id)
        if tarefa:
            tarefa.nome = nome
            tarefa.descricao = descricao
            tarefa.prioridade = prioridade
            tarefa.data_vencimento = data_vencimento
            tarefa.data_hora_inicio = data_hora_inicio
            tarefa.data_hora_fim = data_hora_fim
            self.model._save()
            return True
        return False

    def delete(self, tarefa_id):
        self.model.delete(tarefa_id)

    def toggle_concluida(self, tarefa_id, new_status):
        tarefa = self.model.get_by_id(tarefa_id)
        if tarefa:
            tarefa.isConcluida = new_status
            self.model._save()
            return True
        return False
    
    def _generate_unique_id(self):
        return int(uuid.uuid4().hex[:8], 16)