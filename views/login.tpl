<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/static/css/login.css">
</head>
<body>

<div class="login-box">

    % if error:
        <div class="error">{{error}}</div>
    % end

    <form method="POST">
        <h2>Login</h2>
        <input type="email" name="email" placeholder="Email">
        <input type="password" name="password" placeholder="Senha">
        <button type="submit">Entrar</button>
    </form>

</div>

</body>
</html>
