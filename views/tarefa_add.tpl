%rebase('layout', title='Adicionar Nova Tarefa')

<section class="tasks-section">
    <h1>Adicionar Nova Tarefa</h1>

    <form action="/tarefas/add" method="post">
        
        <label for="nome">Nome:</label>
        <input type="text" id="nome" name="nome" required>

        <label for="descricao">Descrição:</label>
        <textarea id="descricao" name="descricao"></textarea>

        <label for="prioridade">Prioridade:</label>
        <select id="prioridade" name="prioridade">
            <option value="Alta">Alta</option>
            <option value="Média" selected>Média</option>
            <option value="Baixa">Baixa</option>
        </select>
        
        <div class="form-group">
            <label for="data_vencimento">Prazo Final (Data)</label>
            <input type="date" id="data_vencimento" name="data_vencimento">
        </div>
        
        <div class="form-group">
            <label for="hora_inicio_input">Início da Tarefa (Hora)</label>
            <input type="time" id="hora_inicio_input" name="hora_inicio_input">
        </div>

        <div class="form-group">
            <label for="hora_fim_input">Fim da Tarefa (Hora)</label>
            <input type="time" id="hora_fim_input" name="hora_fim_input">
        </div>
        <button type="submit" class="btn btn-primary">Salvar Tarefa</button>
        <a href="/tarefas" class="btn btn-secondary">Cancelar</a>
    </form>
</section>