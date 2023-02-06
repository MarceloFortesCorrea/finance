# settings.py

class Config:
    SECRET_KEY = 'my_secret_key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://pgadmin:marsil07@127.0.0.1:5432/db_dev'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host/dbname'


config_by_name = dict(dev=DevelopmentConfig, prod=ProductionConfig)
