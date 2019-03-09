import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a key'


class DevelopmentConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
}