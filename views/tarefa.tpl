%rebase('layout', title='Tarefas')

<section class="tasks-section">
    <div class="section-header">
        <h1 class="section-title"><i class="fas fa-tasks"></i> Minhas Tarefas</h1>
        <a href="/tarefas/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nova Tarefa
        </a>
    </div>

    <div class="filter-sort-controls">
        <label for="status-filter">Filtrar por Status:</label>
        <select id="status-filter" onchange="applyFilters()">
            <option value="" {{'selected' if not current_status else ''}}>Todas</option>
            <option value="pendente" {{'selected' if current_status == 'pendente' else ''}}>Pendentes</option>
            <option value="concluida" {{'selected' if current_status == 'concluida' else ''}}>Concluídas</option>
        </select>

        <label for="sort-by">Ordenar por:</label>
        <select id="sort-by" onchange="applyFilters()">
            <option value="id" {{'selected' if current_sort == 'id' else ''}}>ID</option>
            <option value="prazo" {{'selected' if current_sort == 'prazo' else ''}}>Prazo (Mais Urgente)</option>
            <option value="prioridade" {{'selected' if current_sort == 'prioridade' else ''}}>Prioridade (Alta -> Baixa)</option>
            <option value="nome" {{'selected' if current_sort == 'nome' else ''}}>Nome (A-Z)</option>
        </select>
    </div>
    
    <div class="table-container">
        <table class="styled-table">
            
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Prioridade</th>
                    <th>Prazo</th> 
                    <th>Duração</th> 
                    <th>Status</th> 
                    <th>Ações</th>
                </tr>
            </thead>

            <tbody>
                % for t in tarefas:
                <tr id="tarefa-row-{{t.id}}" class="{{'concluida' if t.isConcluida else ''}}"> 
                    <td>{{t.id}}</td>
                    <td>{{t.nome}}</td>
                    <td>{{t.descricao}}</td>
                    <td>{{t.prioridade}}</td>
                    
                    <td>
                        % if t.data_vencimento:
                            % parts = t.data_vencimento.split('-')
                            % if len(parts) == 3:
                                {{parts[2]}}/{{parts[1]}}/{{parts[0]}}
                            % else:
                                {{t.data_vencimento}}
                            % end
                        % else:
                            -
                        % end
                    </td>
                    
                    <td>
                        % if t.data_hora_inicio and t.data_hora_fim:
                            {{t.data_hora_inicio[-5:]}} até {{t.data_hora_fim[-5:]}}
                            
                            % if t.duration_hours is not None:
                                <br>({{t.duration_hours}} horas)
                            % end
                        % else:
                            -
                        % end
                    </td>
                    
                    <td>
                        <input 
                            type="checkbox" 
                            class="status-toggle"
                            data-tarefa-id="{{t.id}}"
                            {{'checked' if t.isConcluida else ''}}
                            onchange="toggleTarefaStatus(this)"
                        >
                        <span id="status-label-{{t.id}}">{{'Concluída' if t.isConcluida else 'Pendente'}}</span>
                    </td>
                    
                    <td class="actions">
                        <a href="/tarefas/edit/{{t.id}}" class="btn btn-sm btn-edit">
                            <i class="fas fa-edit"></i> Editar
                        </a>

                        <form action="/tarefas/delete/{{t.id}}" method="post" 
                              onsubmit="return confirm('Tem certeza que deseja excluir esta tarefa?')">
                            <button type="submit" class="btn btn-sm btn-danger">
                                <i class="fas fa-trash-alt"></i> Excluir
                            </button>
                        </form>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    </div>
</section>

<script>
    function applyFilters() {
        const status = document.getElementById('status-filter').value;
        const sortBy = document.getElementById('sort-by').value;
        
        let url = '/tarefas?';
        let params = [];
        
        if (status) {
            params.push(`status=${status}`);
        }
        
        if (sortBy && sortBy !== 'id') {
            params.push(`sort=${sortBy}`);
        }
        
        window.location.href = url + params.join('&');
    }

    function toggleTarefaStatus(checkbox) {
        const tarefaId = checkbox.getAttribute('data-tarefa-id');
        const newStatus = checkbox.checked; 

        fetch(`/tarefas/toggle/${tarefaId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ isConcluida: newStatus }) 
        })
        .then(response => {
            if (!response.ok) {
                checkbox.checked = !newStatus;
                throw new Error('Erro ao atualizar o status.');
            }
            return response.json();
        })
        .then(data => {

            const statusLabel = document.getElementById(`status-label-${tarefaId}`);
            const row = document.getElementById(`tarefa-row-${tarefaId}`);
            
            if (data.isConcluida) {
                statusLabel.textContent = 'Concluída';
                row.classList.add('concluida');
            } else {
                statusLabel.textContent = 'Pendente';
                row.classList.remove('concluida');
            }
        })
        .catch(error => {
            console.error('Falha no toggle de status:', error);
            alert('Falha ao atualizar o status. Verifique o console para mais detalhes.');
        });
    }
</script>