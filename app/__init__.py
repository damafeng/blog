from flask import Flask
from app.routes import main as main_routes
from app.routes.admin import main as admin_routes
from config import config
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()

app = Flask(__name__)
app.config.from_object(config['default'])

bootstrap.init_app(app)
moment.init_app(app)

app.register_blueprint(main_routes)
app.register_blueprint(admin_routes, url_prefix='/admin')

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
    )
    app.run(**config)
