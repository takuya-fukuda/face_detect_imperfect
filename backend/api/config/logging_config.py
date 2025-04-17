import logging
from logging.config import dictConfig
import sys

def setup_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream', # 標準出力にリダイレクト
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        },
        'loggers': {
            'api': {  # apiモジュール専用のLogger
                'level': 'DEBUG',
                'handlers': ['wsgi'],
                'propagate': False,
            },
        }
    }
    dictConfig(logging_config)
