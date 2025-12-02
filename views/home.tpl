% rebase('layout', title='Página Inicial')

<div class="main-container">

    <div class="top-bar">
        <a href="/login" class="btn-login">
            <i class="fas fa-sign-in-alt"></i> Login
        </a>
    </div>

    <div class="home-content">
        <header class="home-header">
            <h1>Bem-vindo ao TaskZ</h1>
            <p>Selecione uma opção abaixo para começar</p>
        </header>

        <div class="dashboard-grid">
            
            <a href="/users" class="dashboard-card">
                <div class="icon-box">
                    <img src="/static/img/usuario.png" alt="Usuários" onerror="this.style.display='none'; this.parentElement.innerHTML='<i class=\'fas fa-users\'></i>'"> 
                </div>
                <h3>Gerenciar Usuários</h3>
                <p>Adicionar, editar e listar usuários.</p>
            </a>

            <a href="/tarefas" class="dashboard-card">
                <div class="icon-box">
                     <img src="/static/img/tarefa.png" alt="Tarefas" onerror="this.style.display='none'; this.parentElement.innerHTML='<i class=\'fas fa-tasks\'></i>'">
                </div>
                <h3>Minhas Tarefas</h3>
                <p>Visualize suas pendências.</p>
            </a>

        </div>
    </div>
</div>