#Animesh Agrawal    animesha    50254531
#Micheal Kirk       kirkmc      49847974
#Rachel Lam         rslam       24554220

from flask import Flask, request, redirect, render_template
from retreiver import Retreiver


r = Retreiver()
print("Loading Index....")
r.open_inverted_index("invertedIndex.json")
print("Ready for use")

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods = ['POST'])
def results():
	query = request.form['searchTerm']
	print(query)
	l = r.list_top_urls(query)
	links = l[0]
	length = l[1]
	if length < 20:
		for i in range(length, 20):
			links.append('')
	return render_template('results.html', res1 = links[0], res2 = links[1], res3 = links[2], res4 = links[3], res5 = links[4], res6 = links[5], \
		res7 = links[6], res8 = links[7], res9 = links[8], res10 = links[9], res11 = links[10], res12 = links[11], res13 = links[12], res14 = links[13], \
		res15 = links[14], res16 = links[15], res17 = links[16], res18 = links[17], res19 = links[18], res20 = links[19])

if __name__ == '__main__':
    app.run()