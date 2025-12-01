from bottle import request
from models.tarefa import TarefaModel, Tarefa

class TarefaService:
    def __init__(self, model: TarefaModel):
        self.model = model

    def get_all(self):
        return self.model.get_all()

    def save(self):
        last_id = max([t.id for t in self.model.get_all()], default=0)
        new_id = last_id + 1

        nome = request.forms.get("nome")
        descricao = request.forms.get("descricao")
        prioridade = request.forms.get("prioridade")
        isConcluida = request.forms.get("isConcluida") == "true"

        tarefa = Tarefa(new_id, nome, descricao, isConcluida, prioridade)
        self.model.add_tarefa(tarefa)

    def get_concluidas(self):
        return self.model.get_concluidas()
    
    def delete(self, tarefa_id):
        tarefa_id = int(tarefa_id)
        self.model.tarefas = [t for t in self.model.tarefas if t.id != tarefa_id]
        self.model._save()

    def get_by_id(self, tarefa_id):
        return self.model.get_by_id(tarefa_id)
