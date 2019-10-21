# -*- coding: utf-8 -*-
import os
from settings import PROJ_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
db = SQLAlchemy()
from apps.files.views import files_bp
from apps.students.views import students_bp
from apps import files
from apps import students


def create_app():
    static_dir = os.path.join(PROJ_DIR, 'static')
    app = Flask(__name__, static_folder=static_dir)

    app.register_blueprint(files_bp, url_prefix='/api/files')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.config['SQLALCHEMY_DATABASE_URI'] \
        = 'mysql+pymysql://root:Ac_superman@127.0.0.1:3306/file_go?charset=utf8mb4'
    app.config['SQLALCHEMY_POOL_SIZE'] = 6
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app, supports_credentials=True, resources=r'/*')
    return app
