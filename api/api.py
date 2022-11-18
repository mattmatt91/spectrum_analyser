from flask import Flask, render_template, redirect, jsonify, request
import spectrumanalyser
from threading import Thread

app = Flask(__name__)
frame = spectrumanalyser.Frame()



@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/features', methods=['POST', 'GET'])
def fetch_data():
	return jsonify(frame.get_data())

@app.route('/update_feature', methods=['GET', 'POST'])
def set_value():
	print('test')
	data = dict(request.json)
	feature_name = data['featureName']
	feature_value = data['value']
	frame.set_feature(feature_name, feature_value)
	return {feature_name: feature_value}






if __name__ == '__main__':
	Thread(target=frame.update).start()
	app.run(debug=False, host='127.0.0.1', port=5000)
