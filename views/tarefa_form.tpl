%rebase('layout', title='Adicionar/Editar Tarefa')

<section class="tasks-section">
    % if 'tarefa' in locals():
        <h1>Editar Tarefa: {{tarefa.nome}}</h1>
        <form action="/tarefas/edit/{{tarefa.id}}" method="post">
    % else:
        <h1>Adicionar Nova Tarefa</h1>
        <form action="/tarefas/add" method="post">
    % end
        
        <label for="nome">Nome:</label>
        <input type="text" id="nome" name="nome" value="{{tarefa.nome if 'tarefa' in locals() else ''}}" required>

        <label for="descricao">Descrição:</label>
        <textarea id="descricao" name="descricao">{{tarefa.descricao if 'tarefa' in locals() else ''}}</textarea>

        <label for="prioridade">Prioridade:</label>
        <select id="prioridade" name="prioridade">
            % for p in ['Alta', 'Média', 'Baixa']:
                <option value="{{p}}" 
                    % if 'tarefa' in locals() and tarefa.prioridade == p:
                        selected
                    % elif 'tarefa' not in locals() and p == 'Média':
                        selected
                    % end
                >{{p}}</option>
            % end
        </select>
        
        <div class="form-group">
            <label for="data_vencimento">Prazo Final (Data)</label>
            <input type="date" 
                   id="data_vencimento" 
                   name="data_vencimento" 
                   value="{{tarefa.data_vencimento if 'tarefa' in locals() else ''}}">
        </div>
        
        <div class="form-group">
            <label for="hora_inicio_input">Início da Tarefa (Hora)</label>
            <input type="time" 
                   id="hora_inicio_input" 
                   name="hora_inicio_input"
                   value="{{tarefa.data_hora_inicio[-5:] if 'tarefa' in locals() and tarefa.data_hora_inicio else ''}}">
        </div>

        <div class="form-group">
            <label for="hora_fim_input">Fim da Tarefa (Hora)</label>
            <input type="time" 
                   id="hora_fim_input" 
                   name="hora_fim_input" 
                   value="{{tarefa.data_hora_fim[-5:] if 'tarefa' in locals() and tarefa.data_hora_fim else ''}}">
        </div>
        <button type="submit" class="btn btn-primary">Salvar Tarefa</button>
        <a href="/tarefas" class="btn btn-secondary">Cancelar</a>
    </form>
</section>