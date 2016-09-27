#!/usr/bin/python

from flask import Flask , jsonify , request
import os

app = Flask( __name__ )

off_str = 'OFF'
on_str = 'ON'

my_state = False

@app.route( '/' )

def index():
    return "Hello, World!"

@app.route( '/api/play/' , methods = [ 'POST' ] )
def play():
    global my_state, off_str , on_str
   
    my_op = request.data.decode( 'utf-8' )
    
  
    
    if my_op == off_str:
        print( 'Off' )
        my_state = False
	os.system( "irsend SEND_ONCE VARILIGHT KEY_POWER2" )
        my_response = 200    
    elif my_op == on_str:
        print( 'On' )
        my_state = True
	os.system( "irsend SEND_ONCE VARILIGHT KEY_POWER" )
        my_response = 200
    else:
        my_response = 400
 
    
    return 'response' , my_response

@app.route( '/api/play/' , methods = [ 'GET' ] )
def status():
    global my_state
    
    if my_state:
        print( 'Returning on' )
        return on_str
    else:
        print( 'Returning off' )
        return off_str

if __name__ == '__main__':
    app.run( debug = True , host = '0.0.0.0' )

