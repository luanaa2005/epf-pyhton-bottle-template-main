% rebase('layout', title='Formulário Usuário')

% if error:
<div style="color:red; font-weight:bold; margin-bottom:10px;">
    {{error}}
</div>
% end
<section class="form-section">
    <h1>{{'Editar Usuário' if user else 'Adicionar Usuário'}}</h1>
    
    <form action="{{action}}" method="post" class="form-container">

        <div class="form-group">
            <label for="name">Nome:</label>
            <input type="text" id="name" name="name" required 
                   value="{{user.name if user else ''}}">
        </div>

        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" {{'required' if not user else ''}}>        
        </div>

        <div class="form-group">
            <label for="password_confirm">Confirmar senha:</label>
            <input type="password" id="password_confirm" name="password_confirm" {{'required' if not user else ''}}>
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required 
                   value="{{user.email if user else ''}}">
        </div>

        <div class="form-group">
            <label for="birthdate">Data de Nascimento:</label>
            <input type="date" id="birthdate" name="birthdate" required 
                   value="{{user.birthdate if user else ''}}">
        </div>
        
        <div class="form-actions">
            <button type="submit" class="btn-submit">Salvar</button>
            <a href="/users" class="btn-cancel">Voltar</a>
        </div>
    </form>
</section>