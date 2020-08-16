from flask import Flask
from . import data
from . import interface


def create_app():
    
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    
    # app.config.from_object('config.Config')
    
    with app.app_context():
        
        # ------------------
        # Include our Routes
        # ------------------
        
        # from . import routes
        
        # -------------------
        # Register Blueprints
        # -------------------
        
        from .interface.fx import fx
        from .interface.home import home

        app.register_blueprint(fx.fx_bp)
        app.register_blueprint(home.home_bp)

        return app