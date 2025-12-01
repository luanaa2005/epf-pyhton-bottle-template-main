%rebase('layout', title='Tarefas')

<section class="tasks-section">
    <div class="section-header">
        <h1 class="section-title"><i class="fas fa-tasks"></i> Minhas Tarefas</h1>
        <a href="/tarefas/add" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nova Tarefa
        </a>
    </div>

    <div class="table-container">
        <table class="styled-table">
            
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Prioridade</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>

            <tbody>
                % for t in tarefas:
                <tr>
                    <td>{{t.id}}</td>
                    <td>{{t.nome}}</td>
                    <td>{{t.descricao}}</td>
                    <td>{{t.prioridade}}</td>
                    <td>{{'Concluída' if t.isConcluida else 'Pendente'}}</td>
                    
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
