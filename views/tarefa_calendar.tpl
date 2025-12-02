%rebase('layout', title=title)
% import datetime

<section class="tasks-section">
    <div class="section-header">
        <h1 class="section-title"><i class="far fa-calendar-alt"></i> Agenda de Tarefas</h1>
        
        <a href="/tarefas" class="btn btn-secondary">
            <i class="fas fa-list"></i> Ver como Lista
        </a>
        <a href="/tarefas/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nova Tarefa
        </a>
    </div>

    <div class="calendar-container">
        % if not tarefas_agrupadas:
        <p>🎉 Nenhuma tarefa com prazo definido encontrada. Adicione uma para começar a agendar!</p>
        % end

        % for data_obj in sorted(tarefas_agrupadas.keys()):
        <div class="calendar-day">
            
            <h3>{{data_obj.strftime("%d/%m/%Y")}}</h3>
            
            <ul class="task-list">
                % for t in tarefas_agrupadas[data_obj]:
                <li class="{{'concluida' if t.isConcluida else 'pendente'}}">
                    <div class="task-details">
                        <span class="task-name">
                            <strong>{{t.nome}}</strong> 
                            <span class="priority-tag priority-{{t.prioridade.lower().replace('ã','a').replace('á','a')}}">
                                ({{t.prioridade}})
                            </span>
                        </span>
                        
                        % if t.data_hora_inicio and t.data_hora_fim:
                        <span class="task-time">
                            {{t.data_hora_inicio[-5:]}} - {{t.data_hora_fim[-5:]}}
                            % if t.duration_hours is not None:
                                <small>({{t.duration_hours}}h)</small>
                            % end
                        </span>
                        % else:
                        <span class="task-time">
                            Dia Inteiro
                        </span>
                        % end

                        <span class="task-actions">
                            <a href="/tarefas/edit/{{t.id}}">Editar</a> |
                            % if not t.isConcluida:
                            <a href="#" onclick="toggleTarefaStatusSimple({{t.id}}, true)">Concluir</a>
                            % else:
                            <span class="status-concluida">Concluída</span>
                            % end
                        </span>
                    </div>
                    <p class="task-description"><small>{{t.descricao}}</small></p>
                </li>
                % end
            </ul>
        </div>
        % end
    </div>
</section>

<script>
    function toggleTarefaStatusSimple(id, newStatus) {
        if (confirm(`Tem certeza que deseja marcar a tarefa ${id} como Concluída?`)) {
            fetch(`/tarefas/toggle/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ isConcluida: newStatus })
            })
            .then(response => {
                if (response.ok) {
                    // Recarrega a página para atualizar o status na agenda
                    window.location.reload(); 
                } else {
                    alert('Erro ao atualizar o status da tarefa.');
                }
            })
            .catch(error => {
                console.error('Falha no toggle de status:', error);
                alert('Falha ao atualizar o status. Verifique o console.');
            });
        }
    }
</script>