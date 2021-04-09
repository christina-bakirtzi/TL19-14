class Config(object):
    SECRET_KEY = '35236712dsgajg1365sg125'
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres', pw='evanescence.',
                                                                                    url='127.0.0.1', db='soft_eng_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


