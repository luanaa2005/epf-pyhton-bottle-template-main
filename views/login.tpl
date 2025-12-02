<form method="POST" action="/login">

    %if error:
    <div class="ERRO">{{error}}</p>
    % end

    <label>Email:</label>
    <input type="email" name="email" required>

    <label>Senha:</label>
    <input type="password" name="password" required>

    <button type="submit">Entrar</button>
</form>
