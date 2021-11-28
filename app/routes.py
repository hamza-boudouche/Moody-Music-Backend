from app import app

@app.route('/')
def index()-> str:
	return "hello world!"