from flask import Flask, render_template, redirect, jsonify
import spectrum_analyser
from threading import Thread

app = Flask(__name__)
frame = spectrum_analyser.Frame()




@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/brightness/<brightness>', methods=['POST', 'GET'])
def setbrightness(brightness):
	brightness = frame.set_brightness(brightness)
	return jsonify(result=brightness)

@app.route('/animation/<animation>', methods=['POST', 'GET'])
def setanimation(animation):
	animation = frame.set_animation(animation)
	return jsonify(result=animation)

@app.route('/render_spec/<render_spec>', methods=['POST', 'GET'])
def setrender_spec(render_spec):
	render_spec = frame.set_render_spec(render_spec)
	return jsonify(result=render_spec)

@app.route('/render_animation/<render_animation>', methods=['POST', 'GET'])
def setrender_animation(render_animation):
	render_animation = frame.set_render_animation(render_animation)
	return jsonify(result=render_animation)

@app.route('/freqarea/<freqarea>', methods=['POST', 'GET'])
def setFreqArea(freqarea): 
	freqarea = frame.set_freq_area(freqarea)
	return jsonify(result=freqarea)

@app.route('/smooth/<smooth>', methods=['POST', 'GET'])
def setsmooth(smooth):
	smooth = frame.set_smooth(smooth)
	return jsonify(result=smooth)

@app.route('/falldown/<falldown>', methods=['POST', 'GET'])
def setfalldown(falldown):
	falldown = frame.set_falldown(falldown)
	return jsonify(result=falldown)

@app.route('/fadespeed/<fadespeed>', methods=['POST', 'GET'])
def setfadespeed(fadespeed): 
	fadespeed = frame.set_fadespeed(fadespeed)
	return jsonify(result=fadespeed)

@app.route('/rainbow/<rainbow>', methods=['POST', 'GET'])
def setrainbow(rainbow):
	rainbow = frame.set_rainbow(rainbow)
	return jsonify(result=rainbow)

@app.route('/yrainbow/<yrainbow>', methods=['POST', 'GET'])
def setyrainbow(yrainbow):
	yrainbow = frame.set_yrainbow(yrainbow)
	return jsonify(result=yrainbow)

@app.route('/sym/<sym>', methods=['POST', 'GET'])
def setsym(sym):
	sym = frame.set_sym(sym)
	return jsonify(result=sym)

@app.route('/maxdot/<maxdot>', methods=['POST', 'GET'])
def setmaxdot(maxdot): 
	maxdot = frame.set_maxdot(maxdot)
	return jsonify(result=maxdot)

@app.route('/blackspec/<blackspec>', methods=['POST', 'GET'])
def setblackspec(blackspec):
	blackspec = frame.set_blackspec(blackspec)
	return jsonify(result=blackspec)

@app.route('/center/<center>', methods=['POST', 'GET'])
def setcenter(center):
	center = frame.set_center(center)
	return jsonify(result=center)

if __name__ == '__main__':
	Thread(target=frame.update).start()
	app.run(host='0.0.0.0')
