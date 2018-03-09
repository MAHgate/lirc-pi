#!/usr/bin/python3

from flask import Flask , jsonify , request
import os

# Lots of actions

class Action( object ):
	def __init__( self , name ):
		self.name = name
		self.code = 'SEND_ONCE'
		self.key = name
		self.option_list = []

	def set_key( self , key ):
		self.key = key

	def set_code( self , code ):
		self.send = code

# So we can label devices

class Device( object ):
	def __init__( self , name ):
		self.name = name
		self.full_name = name
		self.actions = []
		self.room = None

	def add_action( self , action ):
		self.actions.append( action )
	
	def add_room( self , room ):
		self.room = room

# So we can label rooms

class Room( object ):
	def __init__( self ,name ):
		self.name = name
		self.full_name = name

# Create our rooms (not sure if this helps)

Lounge = Room( 'Lounge' )
Hallway = Room( 'Hallway' )
Ellie = Room( 'Ellie' )

room_list = [ Lounge , Hallway , Ellie ]

# Set up Azur AMP ( we should do this with XML )

Azur = Device( 'AZUR' )

azur_list = [ 'Tape_mon' , 'KEY_DVD' , 'AV_MD' , 'Tuner_DAB' , 'Aux_phono' , 'KEY_CD' , 'KEY_MUTE' , 'KEY_VOLUMEUP' , 'KEY_VOLUMEDOWN' ]

azur_cmd = 'none'

for a in azur_list:
	Azur.add_action( Action( a ) )

# Put devices in alist

device_list = [ Azur ]

# Start the App

app = Flask( __name__ )

# On and Off jokes

off_str = 'OFF'
on_str = 'ON'

loungelights_state = False

# Root response is just a Hello World

@app.route( '/' )

def index():
	return "Hello, World!"

# My loungelights controller

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

# Original Azur routine. Now unnecessary

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
	

# Loungelights state

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

# More redundant Azur

@app.route( '/api/azur/' , methods = [ 'GET' ] )
def azur_status():
	global azur_cmd
	return 'Last command sent: '+azur_cmd
 
# Default response to a get is just to return the last successful command

@app.route( '/<room>/<devicename>/' , methods = [ 'GET' ] )
def device_status( room , devicename ):
	return cmd + '\n'

# Trying to get a bit more generic

@app.route( '/<room_name>/<device_name>/' , methods = [ 'POST' ] )
def apply_action( room_name , device_name ):
	global device_list , room_list

	my_op = request.form.get( 'command' )

	print( room_name , device_name , my_op )
	
	my_room = None

	for r in room_list:
		if r.name == room_name:
			my_room = r
	
	my_device = None
	
	for d in device_list:
		if d.name == device_name:
			my_device = d
	
	if my_room and my_device:
		my_action = None
		
		for a in my_device.actions:
			if a.name == my_op:
				my_action = a
		
		if my_action:
			cmd = 'irsend ' + my_action.code + ' ' + my_device.name + ' ' + my_action.key
			os.system( cmd )
			print( cmd )
			return cmd + '\n'
		else:
			return 'Action ' + my_op + ' not understood.\n'

	else:	
		return_str = ''
		if my_room:
			return_str += 'Room: ' + room_name + '\n'
		else:
			return_str += 'No such room: ' + room_name + '\n'
		
		if my_device:
			return_str += 'Device: ' + device_name + '\n'
		else:
			return_str += 'No such device: ' + device_name + '\n' 		

		return return_str

# Nice trick

if __name__ == '__main__':
	app.run( debug = True , host = '0.0.0.0' )
	


