from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "123"

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html') 

if __name__ == '__main__':
	app.run(debug=True)
