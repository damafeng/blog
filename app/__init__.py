from flask import Flask
from app.routes import main as main_routes
from config import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(config['default'])

bootstrap.init_app(app)

app.register_blueprint(main_routes)

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
    )
    app.run(**config)
