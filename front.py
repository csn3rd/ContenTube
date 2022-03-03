from flask import Flask, render_template, send_from_directory, request
import string
from back import tedtalk
from back import random_talk

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
	query = request.form['input']
	corpus = request.form['corpus']

	try:
		assert('c' in query)
		res = []

		if corpus == "t":
			# tf-idf on title
			for i in range (10):
				res += [random_talk()]
		elif corpus == "d":
			# tf-idf on description
			for i in range (10):
				res += [random_talk()]
		elif corpus == "c":
			# tf-idf on transcript
			for i in range (10):
				res += [random_talk()]
		else:
			raise Exception('someone is trying to hack the corpus')

		print(res)
		return render_template('index.html', input=query, corpus=corpus, success=True, results=res)
	except:
		return render_template('index.html', input=query, corpus=corpus, success=False)

@app.route('/about', methods=['GET'])
def about():
	return send_from_directory('static','about.html')

if __name__ == '__main__':
	app.debug = True
	app.run()