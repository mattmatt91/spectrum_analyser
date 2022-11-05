@app.route('/center/<center>', methods=['POST', 'GET'])
def setcenter(center):
	# function 
	print ("center: {}".format(center))
	return jsonify(result=center)