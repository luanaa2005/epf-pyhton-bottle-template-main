%rebase('layout', title='Nova Tarefa')

<section class="tasks-section">
    <h1>Adicionar Nova Tarefa</h1>

    <form action="/tarefas/add" method="post">
        <label>Nome:</label>
        <input type="text" name="nome" required>

        <label>Descrição:</label>
        <textarea name="descricao"></textarea>

        <label>Prioridade:</label>
        <select name="prioridade">
            <option value="Alta">Alta</option>
            <option value="Média">Média</option>
            <option value="Baixa">Baixa</option>
        </select>

        <label>Status:</label>
        <select name="isConcluida">
            <option value="false">Pendente</option>
            <option value="true">Concluída</option>
        </select>

        <button type="submit" class="btn btn-primary">Salvar</button>
    </form>
</section>
