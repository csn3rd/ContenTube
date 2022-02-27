from flask import Flask, render_template, request
import random, string

def randomword(length):
   letters = string.ascii_lowercase+(' '*5)
   return ''.join(random.choice(letters) for i in range(length))


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
	query = request.form['input']
	corpus = request.form['corpus']

	try:
		assert('e' in query)
		res = []

		if corpus == "t":
			# tf-idf on title
			for i in range (10):
				res += [temp(randomword(120),randomword(700))]
		elif corpus == "d":
			# tf-idf on description
			for i in range (10):
				res += [temp(randomword(120),randomword(700))]
		elif corpus == "c":
			# tf-idf on transcript
			for i in range (10):
				res += [temp(randomword(120),randomword(700))]
		else:
			raise Exception('someone is trying to hack the corpus')

		return render_template('index.html', input=query, corpus=corpus, success=True, results=res)
	except:
		return render_template('index.html', input=query, corpus=corpus, success=False)

if __name__ == '__main__':
	app.debug = True
	app.run()

class temp:
	def __init__(self,t,d):
		self.title = t
		self.description = d

	def __repr__(self):
		return "(" + self.title + " " + self.description + ")"

	def __str__(self):
		return "(" + self.title + " " + self.description + ")"