%rebase('layout', title='Nova Tarefa')

<section class="form-section">
    <h1 class="section-title"><i class="fas fa-plus"></i> Criar Nova Tarefa</h1>

    <form action="/tarefas/add" method="post" class="styled-form">

        <label for="nome">Nome da Tarefa</label>
        <input type="text" id="nome" name="nome" required>

        <label for="descricao">Descrição</label>
        <textarea id="descricao" name="descricao" rows="3" required></textarea>

        <label for="prioridade">Prioridade</label>
        <select id="prioridade" name="prioridade">
            <option value="Baixa">Baixa</option>
            <option value="Média">Média</option>
            <option value="Alta">Alta</option>
        </select>

        <button type="submit" class="btn btn-primary">
            <i class="fas fa-check"></i> Salvar
        </button>

        <a href="/tarefas" class="btn btn-secondary">Cancelar</a>
    </form>
</section>
