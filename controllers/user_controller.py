from bottle import Bottle, request
from .base_controller import BaseController
from services.user_service import UserService
from models.user import User

class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/users', method='GET', callback=self.list_users)
        self.app.route('/users/add', method=['GET', 'POST'], callback=self.add_user)
        self.app.route('/users/edit/<user_id:int>', method=['GET', 'POST'], callback=self.edit_user)
        self.app.route('/users/delete/<user_id:int>', method='POST', callback=self.delete_user)
        self.app.route('/login', method=['GET', 'POST'], callback=self.login)

    def list_users(self):
        users = self.user_service.get_all()
        return self.render('users', users=users)

    def add_user(self):
        if request.method == 'GET':
            return self.render('user_form', user=None, action="/users/add", error=None)
        else:
            error = self.user_service.save()
            if error:
                temp_user = User(
                    id=None,
                    name=request.forms.get('name'),
                    email=request.forms.get('email'),
                    birthdate=request.forms.get('birthdate'),
                    password=""
                )
                return self.render('user_form', user=temp_user, action="/users/add", error=error)
            
            return self.redirect('/users')

    def edit_user(self, user_id):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == 'GET':
            return self.render('user_form', user=user, action=f"/users/edit/{user_id}", error=None)
        
        form_data = {
            "name": request.forms.get('name'),
            "email": request.forms.get('email'),
            "birthdate": request.forms.get('birthdate'),
            "password": request.forms.get('password'),
            "password_confirm": request.forms.get('password_confirm')
        }

        error = self.user_service.edit_user(user_id, form_data)
        if error:
            temp_user = User(
                id=user_id,
                name=form_data["name"],
                email=form_data["email"],
                birthdate=form_data["birthdate"],
                password=""
            )
            return self.render('user_form', user=temp_user, action=f"/users/edit/{user_id}", error=error)
        
        return self.redirect('/users')

    def delete_user(self, user_id):
        self.user_service.delete_user(user_id)
        return self.redirect('/users')

    def login(self):
        if request.method == 'GET':
            return self.render('login', error=None)

        email = request.forms.get('email')
        password = request.forms.get('password')

        user = self.user_service.authenticate(email, password)
        if not user:
            return self.render('login', error="Email ou senha incorretos")

        request.environ['user'] = user
        return self.redirect('/users')

user_routes = Bottle()

def load_controller():
    return UserController(user_routes)