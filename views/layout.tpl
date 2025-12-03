<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Bottle - {{title or 'Sistema'}}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="/static/css/users.css" />
    <link rel="stylesheet" href="/static/css/home.css" />
    <link rel="stylesheet" href="/static/css/login.css" />
    <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body style="margin: 0; padding: 0;">

    % if title != 'Login':
    <nav class="main-nav">
        <div class="nav-container">
            <a href="/" class="brand">TaskZ</a>
            <div class="nav-links">
                <a href="/"><i class="fas fa-home"></i> Início</a>
                <a href="/tarefas"><i class="fas fa-tasks"></i> Tarefas</a>
                <a href="/users"><i class="fas fa-users"></i> Usuários</a>
                <a href="/login" class="logout"><i class="fas fa-sign-out-alt"></i> Sair</a>
            </div>
        </div>
    </nav>
    % end


    <div class="container">
        {{!base}} 
    </div>

    <!-- Scripts JS no final do body -->
    <script src="/static/js/main.js"></script>
</body>
</html>
