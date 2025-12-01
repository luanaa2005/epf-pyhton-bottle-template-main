import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Tarefa:
    def __init__(self, id, nome, descricao, isConcluida, prioridade):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.isConcluida = isConcluida
        self.prioridade = prioridade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "isConcluida": self.isConcluida,
            "prioridade": self.prioridade
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["nome"],
            data["descricao"],
            data["isConcluida"],
            data["prioridade"]
        )


class TarefaModel:
    FILE_PATH = os.path.join(DATA_DIR, "tarefas.json")

    def __init__(self):
        self.tarefas = self._load()

    def _load(self):
    # Se o arquivo não existe → lista vazia
        if not os.path.exists(self.FILE_PATH):
            return []

    # Se o arquivo existe mas está vazio → lista vazia
        if os.path.getsize(self.FILE_PATH) == 0:
            return []

    # Tenta carregar o JSON
        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Tarefa.from_dict(item) for item in data]
        except json.JSONDecodeError:
        # Arquivo corrompido → retorna lista vazia
            return []

        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Tarefa.from_dict(item) for item in data]
            except json.JSONDecodeError:
                return []

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, indent=4)

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
