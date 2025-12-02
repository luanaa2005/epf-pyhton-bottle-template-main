
from bottle import request
from models.user import UserModel, User

class UserService:
    def __init__(self):
        self.user_model = UserModel()


    def get_all(self):
        users = self.user_model.get_all()
        return users


    def save(self):
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')
        password = request.forms.get('password')
        password_confirm = request.forms.get('password_confirm')

        if password != password_confirm:
            return "Erro: senhas não coincidem"


        user = User(id=new_id, name=name, email=email, birthdate=birthdate, password=password)
        self.user_model.add_user(user)


    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)


    def edit_user(self, user, form):
        name = form["name"]
        email = form["email"]
        birthdate = form["birthdate"]
        password = form["password"]
        password_confirm = form["password_confirm"]

        user.name = name
        user.email = email
        user.birthdate = birthdate

        if password:
            if password != password_confirm:
                return "Erro: senhas não coincidem"
            user.password = password
        self.user_model.update_user(user)

    def authenticate(self, email, password):
        users = self.user_model.get_all()
        for user in users:
            if user.email == email and user.password == password:
                return user
        return None

    def delete_user(self, user_id):
        self.user_model.delete_user(user_id)
