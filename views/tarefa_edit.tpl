%rebase('layout', title='Editar Tarefa')

<section class="add-task-section">
    <div class="section-header">
        <h1 class="section-title"><i class="fas fa-edit"></i> Editar Tarefa: {{tarefa.nome}}</h1>
    </div>

    <form action="/tarefas/edit/{{tarefa.id}}" method="post" class="styled-form">
        
        <div class="form-group">
            <label for="nome">Nome da Tarefa</label>
            <input type="text" id="nome" name="nome" value="{{tarefa.nome}}" required>
        </div>

        <div class="form-group">
            <label for="descricao">Descrição</label>
            <textarea id="descricao" name="descricao">{{tarefa.descricao}}</textarea>
        </div>

        <div class="form-group">
            <label for="prioridade">Prioridade</label>
            <select id="prioridade" name="prioridade" required>
                <option value="Baixa" {{'selected' if tarefa.prioridade == 'Baixa' else ''}}>Baixa</option>
                <option value="Média" {{'selected' if tarefa.prioridade == 'Média' else ''}}>Média</option>
                <option value="Alta" {{'selected' if tarefa.prioridade == 'Alta' else ''}}>Alta</option>
            </select>
        </div>

        <div class="form-group">
            <label for="data_vencimento">Prazo Final (Data)</label>
            <input type="date" id="data_vencimento" name="data_vencimento" value="{{tarefa.data_vencimento if tarefa.data_vencimento else ''}}">
        </div>
        
        <div class="form-group">
            <label for="data_hora_inicio">Início da Tarefa (Data e Hora)</label>
            <input type="datetime-local" id="data_hora_inicio" name="data_hora_inicio" 
                   value="{{tarefa.data_hora_inicio if tarefa.data_hora_inicio else ''}}">
        </div>

        <div class="form-group">
            <label for="data_hora_fim">Fim da Tarefa (Data e Hora)</label>
            <input type="datetime-local" id="data_hora_fim" name="data_hora_fim"
                   value="{{tarefa.data_hora_fim if tarefa.data_hora_fim else ''}}">
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-success"><i class="fas fa-save"></i> Atualizar Tarefa</button>
            <a href="/tarefas" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Voltar</a>
        </div>
    </form>
</section>