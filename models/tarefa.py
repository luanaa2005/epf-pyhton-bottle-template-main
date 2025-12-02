import json
import os
from datetime import date, datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Tarefa:
    def __init__(self, id, nome, descricao, isConcluida, prioridade, 
                 data_vencimento=None, data_hora_inicio=None, data_hora_fim=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.isConcluida = isConcluida
        self.prioridade = prioridade
        self.data_vencimento = data_vencimento 
        self.data_hora_inicio = data_hora_inicio 
        self.data_hora_fim = data_hora_fim       

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "isConcluida": self.isConcluida,
            "prioridade": self.prioridade,
            "data_vencimento": self.data_vencimento,
            "data_hora_inicio": self.data_hora_inicio,
            "data_hora_fim": self.data_hora_fim
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["nome"],
            data["descricao"],
            data["isConcluida"],
            data["prioridade"],
            data.get("data_vencimento"),
            data.get("data_hora_inicio"), 
            data.get("data_hora_fim")
        )


class TarefaModel:
    FILE_PATH = os.path.join(DATA_DIR, "tarefas.json")
    
    
    PRIORITY_ORDER = {"Alta": 3, "Média": 2, "Baixa": 1}

    def __init__(self):
        self.tarefas = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH) or os.path.getsize(self.FILE_PATH) == 0:
            return []

        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Tarefa.from_dict(item) for item in data]
        except json.JSONDecodeError:
            return [] 

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.tarefas
    
    def get_by_id(self, tarefa_id):
        return next((t for t in self.tarefas if t.id == tarefa_id), None)

    def get_concluidas(self):
        return [t for t in self.tarefas if t.isConcluida == True]

    def add_tarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)
        self._save()

    def delete(self, tarefa_id):
        self.tarefas = [t for t in self.tarefas if t.id != tarefa_id]
        self._save()

    
    def get_filtered_and_sorted(self, status=None, sort_by='id'):
        
        tarefas_filtradas = self.tarefas

        
        if status:
            status = status.lower()
            if status == 'pendente':
                tarefas_filtradas = [t for t in tarefas_filtradas if not t.isConcluida]
            elif status == 'concluida':
                tarefas_filtradas = [t for t in tarefas_filtradas if t.isConcluida]

        
        if sort_by == 'prazo':
            def sort_key(t):
                if t.data_vencimento:
                    try:
                        
                        if t.data_hora_fim:
                            return datetime.strptime(t.data_hora_fim, '%Y-%m-%dT%H:%M')
                        return datetime.strptime(t.data_vencimento, '%Y-%m-%d')
                    except ValueError:
                        return datetime.max 
                return datetime.max
            
            
            tarefas_filtradas.sort(key=sort_key) 
            
        elif sort_by == 'prioridade':
            tarefas_filtradas.sort(key=lambda t: self.PRIORITY_ORDER.get(t.prioridade, 0), reverse=True)
            
        elif sort_by == 'nome':
            tarefas_filtradas.sort(key=lambda t: t.nome.lower())
            
        
        else: 
            tarefas_filtradas.sort(key=lambda t: t.id)
            

        return tarefas_filtradas