from bottle import Bottle, static_file
from config import Config
import os
from controllers import init_controllers
class App:
    def __init__(self):
        self.bottle = Bottle()
        self.config = Config()

    def setup_routes(self):
        print('🚀 Inicializando Sistema...')
        
        init_controllers(self.bottle)

        @self.bottle.route('/static/<filepath:path>')
        def serve_static(filepath):
            base_path = os.path.dirname(os.path.abspath(__file__))
            static_path = os.path.join(base_path, 'static')
            return static_file(filepath, root=static_path)

        print("\n--- ROTAS ATIVAS ---")
        for route in self.bottle.routes:
            print(f"👉 {route.method} {route.rule}")
        print("--------------------\n")

    def run(self):
        self.setup_routes()
        self.bottle.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG,
            reloader=self.config.RELOADER
        )

def create_app():
    return App()

if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run()