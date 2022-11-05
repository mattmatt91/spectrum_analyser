from flask import Flask, render_template, redirect, jsonify
from ledstrip_test import ledstrip
import spectrum_analyser
from threading import Thread

app = Flask(__name__)
frame = spectrum_analyser.Frame()




@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/brightness/<brightness>', methods=['POST', 'GET'])
def setbrightness(brightness):
	frame.set_brightness(brightness)
	print ("brightness: {}".format(brightness))
	return jsonify(result=brightness)

@app.route('/freqarea/<freqarea>', methods=['POST', 'GET'])
def setFreqArea(freqarea): 
	frame.set_freq_area(freqarea)
	print ("Freqarea: {}".format(freqarea))
	return jsonify(result=freqarea)

@app.route('/smooth/<smooth>', methods=['POST', 'GET'])
def setSmooth(smooth):
	frame.set_smooth(smooth)
	print ("Smooth: {}".format(smooth))
	return jsonify(result=smooth)

@app.route('/falldown/<falldown>', methods=['POST', 'GET'])
def setfalldown(falldown):
	frame.set_falldown(falldown)
	print ("falldown: {}".format(falldown))
	return jsonify(result=falldown)

@app.route('/fadespeed/<fadespeed>', methods=['POST', 'GET'])
def setfadespeed(fadespeed): 
	frame.set_fadespeed(fadespeed)
	print ("fadespeed: {}".format(fadespeed))
	return jsonify(result=fadespeed)

@app.route('/rainbow/<rainbow>', methods=['POST', 'GET'])
def setrainbow(rainbow):
	frame.set_rainbow(rainbow)
	print ("rainbow: {}".format(rainbow))
	return jsonify(result=rainbow)

@app.route('/yrainbow/<yrainbow>', methods=['POST', 'GET'])
def setyrainbow(yrainbow):
	frame.set_yrainbow(yrainbow)
	print ("yrainbow: {}".format(yrainbow))
	return jsonify(result=yrainbow)

@app.route('/sym/<sym>', methods=['POST', 'GET'])
def setsym(sym):
	frame.set_sym(sym)
	print ("sym: {}".format(sym))
	return jsonify(result=sym)

@app.route('/maxdot/<maxdot>', methods=['POST', 'GET'])
def setmaxdot(maxdot): 
	frame.set_maxdot(maxdot)
	print ("maxdot: {}".format(maxdot))
	return jsonify(result=maxdot)

@app.route('/blackspec/<blackspec>', methods=['POST', 'GET'])
def setblackspec(blackspec):
	frame.set_blackspec(blackspec)
	print ("blackspec: {}".format(blackspec))
	return jsonify(result=blackspec)

@app.route('/center/<center>', methods=['POST', 'GET'])
def setcenter(center):
	frame.set_center(center)
	print ("center: {}".format(center))
	return jsonify(result=center)

if __name__ == '__main__':
	Thread(target=frame.update).start()
	app.run(host='0.0.0.0')
