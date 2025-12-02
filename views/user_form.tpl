% rebase('layout', title='Formulário Usuário')

<section class="form-section">
    <h2>{{'Editar Usuário' if user else 'Adicionar Usuário'}}</h2>

% if error:
<div class="error">
    {{error}}
</div>
% end

<form action="{{action}}" method="post">
   
        <div class="form-group">
            <label for="name">Nome:</label>
            <input type="text" id="name" name="name" required 
                   value="{{user.name if user else ''}}" placeholder="Digite aqui seu nome">
        </div>

        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" {{'required' if not user else ''}} placeholder="********">        
        </div>

        <div class="form-group">
            <label for="password_confirm">Confirmar senha:</label>
            <input type="password" id="password_confirm" name="password_confirm" {{'required' if not user else ''}} placeholder="********">
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required 
                   value="{{user.email if user else ''}}" placeholder="Digite aqui seu email">
        </div>

        <div class="form-group">
            <label for="birthdate">Data de Nascimento:</label>
            <input type="date" id="birthdate" name="birthdate" required 
                   value="{{user.birthdate if user else ''}}">
        </div>
        
        <div class="button-group">
            <a href="/users" class="button-cancel">Voltar</a>
            <button type="submit">Salvar</button>
        </div>
    </form>
</section>
