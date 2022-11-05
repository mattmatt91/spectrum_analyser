from flask import Flask, render_template, redirect, jsonify
from ledstrip_test import ledstrip
import spectrum_analyser
from threading import Thread

app = Flask(__name__)
leds = ledstrip()


FREQ_AREA = 20  # win size of raw data --> change in UI # size of array for one band at matrix
SMOOTH = 3  # high value is slow fall --> change in UI
FALLDOWN = 7  # high value is slow fall --> change in UI
FADESPEED = 5  # color change speed, high value is lsow speed --> change in UI
RAINBOW = 4  # 255//BANDS  # gradient of colors for x axis --> change in UI
YRAINBOW = 20 # 255//BANDS  # gradient of colors for y axis --> change in UI
SYM = True # --> change in UI
MAXDOT = True# draw max dot  --> change in UI
BLACKSPEC = False # --> change in UI
CENTER = False # when sym is true, drw center or borders --> change in UI

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/on', methods=['POST', 'GET'])
def on():
	print('On')
	leds.on()
	return jsonify(result="On")

@app.route('/off', methods=['POST', 'GET'])
def off():
	print('Off')
	leds.off()
	return jsonify(result="Off")

@app.route('/freqarea/<freqarea>', methods=['POST', 'GET'])
def setColor(freqarea):
	# function 
	print ("Freqarea: {}".format(freqarea))
	return jsonify(result=freqarea)

if __name__ == '__main__':
	frame = spectrum_analyser.Frame()
	Thread(target=frame.update).start()
	# app.run(host='0.0.0.0')
