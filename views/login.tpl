% rebase('layout', title='Login')

<div class="login-wrapper">
    
    <div class="login-box">
        <h2>Login</h2>

        % if error:
            <div class="login-error">
                <i class="fas fa-exclamation-circle"></i> {{error}}
            </div>
        % end

        <form action="/login" method="POST">
            
            <input type="email" name="email" placeholder="Digite seu email" required>
            
            <input type="password" name="password" placeholder="Sua senha" required>
            
            <button type="submit" class="btn-login-submit">Entrar</button>
        </form>

    </div>
</div>