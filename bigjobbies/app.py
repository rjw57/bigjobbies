import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('bigjobbies.default_settings')
if 'BIGJOBBIES_SETTINGS' in os.environ:
    app.config.from_envvar('BIGJOBBIES_SETTINGS')

