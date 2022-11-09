from flask import Flask, render_template, redirect, jsonify
import spectrum_analyser
from threading import Thread

app = Flask(__name__)
frame = spectrum_analyser.Frame()



@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/data/', methods=['POST', 'GET'])
def fetch_data():
	return jsonify(frame.get_data())

@app.route('/feature/<feature>/<value>', methods=['POST', 'GET'])
def set_value(feature, value):
	val = frame.set_feature(feature, value)
	print(val)
	return jsonify(result=val)



if __name__ == '__main__':
	Thread(target=frame.update).start()
	app.run(host='0.0.0.0')
