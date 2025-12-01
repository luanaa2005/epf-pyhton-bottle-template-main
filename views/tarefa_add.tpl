%rebase('layout', title='Adicionar Tarefa')

<section class="tasks-section">
    <div class="section-header">
        <h1 class="section-title">
            <i class="fas fa-plus-circle"></i> Nova Tarefa
        </h1>
        <a href="/tarefas" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>

    <div class="form-container">
        <form action="/tarefas/add" method="post" class="styled-form">

            <div class="form-group">
                <label for="nome">Nome da Tarefa</label>
                <input type="text" id="nome" name="nome" required placeholder="Ex: Estudar Python">
            </div>

            <div class="form-group">
                <label for="descricao">Descrição</label>
                <textarea id="descricao" name="descricao" rows="3" placeholder="Detalhes da tarefa"></textarea>
            </div>

            <div class="form-group">
                <label for="prioridade">Prioridade</label>
                <select id="prioridade" name="prioridade" required>
                    <option value="Baixa">Baixa</option>
                    <option value="Média">Média</option>
                    <option value="Alta">Alta</option>
                </select>
            </div>

            <div class="form-group checkbox-group">
                <label>
                    <input type="checkbox" name="isConcluida">
                    Marcar como concluída
                </label>
            </div>

            <button type="submit" class="btn btn-primary">
                <i class="fas fa-save"></i> Salvar Tarefa
            </button>
        </form>
    </div>
</section>

<style>
    .form-container {
        margin-top: 20px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        background: #fff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    .styled-form .form-group {
        margin-bottom: 20px;
    }

    .styled-form label {
        display: block;
        margin-bottom: 6px;
        font-weight: bold;
    }

    .styled-form input,
    .styled-form select,
    .styled-form textarea {
        width: 100%;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 1rem;
    }

    .checkbox-group label {
        font-weight: normal;
    }

    .btn {
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
    }
</style>
