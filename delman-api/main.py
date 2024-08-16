from app import create_app
from config import Config

app = create_app()

@app.route('/')
def home():
    return {'message': 'Welcome to the Delman API'}, 200

if __name__ == '__main__':
    app.run(port=Config.PORT, debug=True)
