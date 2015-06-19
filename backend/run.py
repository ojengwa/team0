from app import app

app.run(host=app.config['SERVER_SETTINGS']['host'],
        port=app.config['SERVER_SETTINGS']['port'],
        debug=app.config['SERVER_SETTINGS']['debug'])

