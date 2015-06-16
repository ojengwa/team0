from app import app

@app.route('/')
def it_works():
    return 'it works!'
