#!/usr/bin/python3

from flask import Flask , jsonify , request
import os

azur_list = [ 'Tape_mon' , 'KEY_DVD' , 'AV_MD' , 'Tuner_DAB' , 'Aux_phono' , 'KEY_CD' , 'KEY_MUTE' , 'KEY_VOLUMEUP' , 'KEY_VOLUMEDOWN' ]
azur_cmd = 'none'

app = Flask( __name__ )

off_str = 'OFF'
on_str = 'ON'

loungelights_state = False

@app.route( '/' )

def index():
	return "Hello, World!"

@app.route( '/api/loungelights/' , methods = [ 'POST' ] )
def loungelights():
	global loungelights_state, off_str , on_str
   
	#my_op = request.data.decode( 'utf-8' )
	
	my_op = request.form.get( 'state' )
	
	print( 'Request info:' ,my_op )  

	if my_op == off_str:
		print( 'Off' )
		loungelights_state = False
		os.system( "irsend SEND_ONCE VARILIGHT KEY_POWER2" )
		my_response = 200    
	elif my_op == on_str:
		print( 'On' )
		loungelights_state = True
		os.system( "irsend SEND_ONCE VARILIGHT KEY_POWER" )
		my_response = 200
	else:
		my_response = 400
 
    
	return 'response' , my_response

@app.route( '/api/azur/' , methods = [ 'POST' ] )
def azur():
	global azur_list , azur_cmd

	my_op = request.form.get( 'command' )
	
	print( 'Request info:' , my_op )

	if my_op in azur_list:
		os.system( 'irsend SEND_ONCE AZUR ' +my_op )
		azur_cmd = my_op
		return 'Sent '+my_op
	else:
		azur_cmd = 'Error, no command ' + my_op
		return 'No such command. Try\n' + '\n'.join( azur_list ) + '\n'
	


@app.route( '/api/loungelights/' , methods = [ 'GET' ] )
def status():
	global loungelights_state
    	
	state_string = 'Current lounge lighting status: '
	
	if loungelights_state:
		print( 'Returning on' )
		state_string += 'on.'
	else:
		print( 'Returning off' )
		state_string += 'off.'

	return state_string	

@app.route( '/api/azur/' , methods = [ 'GET' ] )
def azur_status():
	global azur_cmd
	return 'Last command sent: '+azur_cmd
 
@app.route( '/<room>/<devicename>' , methods = [ 'GET' ] )
def device_status( room , devicename ):
	return 'You chose location ' + room + ' and device ' + devicename
	
if __name__ == '__main__':
	app.run( debug = True , host = '0.0.0.0' )
