from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
import iperf3
import json
import os
import logging

#app basic config
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'Put your user here'
app.config['BASIC_AUTH_PASSWORD'] = 'Put your password here'
basic_auth = BasicAuth(app)

#Iperf default server
iperf_server='bouygues.iperf.fr'
iperf_s_port=5200

#App logging configuration
try:
    Logs_directory = os.environ['CAF_APP_LOG_DIR'] + "/"
except KeyError as e:
    # print(str(e) + " is non-existent")
    Logs_directory = "./"

strmhandler = logging.StreamHandler()
strmhandler.setLevel(logging.DEBUG)
app.logger.addHandler(strmhandler)
app.logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(Logs_directory + 'webapp.log')
file_handler.setLevel(logging.DEBUG)
gunicorn_logger = logging.getLogger('gunicorn.error')
gunicorn_logger.addHandler(file_handler)





#Index page of the app 
@app.route('/')
def index():
	html = """
	<!doctype html>
	<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>CISCO IoX Iperf demo</title>
	</head>
	<body>
		<h1>CISCO IoX Iperf demo</h1>
		<p>This is an IoT docker container demo for cisco IoX, use the API to access the demo</p>
		<h2>API endpoints:</h2>
		<p>Use basic auth with the provided username and paswword for all calls</p>
		<ul>
			<li style="color:DodgerBlue;"><strong>Config:</strong> POST /config</li>
			<p style="color:Gray;">Connfigure the Iperf server host and port default bouygues.iperf.fr:5200</br>
			Reqest format: { "iperf": {"host":"0.0.0.0","port":"5200"} }</p>
			<li style="color:DodgerBlue;"><strong>Iperf:</strong> GET /iperf</li>
			<p style="color:Gray;">Run Iperf and return network link proprties</p>		
		</ul>		
	</body>
	</html>
	"""
	app.logger.info("Served")
	return html

#Config API endpoint 
@app.route('/config', methods=['POST'])
@basic_auth.required
def config():
	#JSON format {'iperf':{'host':'0.0.0.0','port':'5200'}}
	global iperf_server,iperf_s_port
	if not request.json or not 'iperf' in request.json:
		abort(400)
		app.logger.warning('worong reqest aborting')
	try:
		iperf_server = request.json['iperf']['host']
		iperf_s_port=request.json['iperf']['port']
	except Exception as e:
		status='exception'
		data='server error: '+str(e)
		app.logger.exception(str(e))
	else:
		status="updated"
		data=request.json['iperf']
	finally:
		app.logger.info("Iperf server updated")
		return jsonify({'status':status, 'data':data }), 200


#Iperf API endoint to lunch link tests
@app.route('/iperf', methods=['GET'])
@basic_auth.required
def iperf():
	client = iperf3.Client()
	client.duration = 1
	client.server_hostname = iperf_server
	client.port = iperf_s_port
	try:
		result = client.run()
	except Exception as e:
		status='exception'
		r=str(e)
	else:
		print(result.error)
		if result.error == None:
			status='success'
			r=result.json
		else:
			status='error'
			r=result.error
	finally:
		app.logger.info("Iperf test end")
		return jsonify({'status':status,'data': r}), 200





if __name__ == '__main__':
	app.run(debug=True)
