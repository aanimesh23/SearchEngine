from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods = ['POST'])
def results():
	query = request.form['searchTerm']
	print(query)
	return render_template('results.html')

if __name__ == '__main__':
    app.run()