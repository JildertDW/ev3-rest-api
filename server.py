#!/usr/bin/env python
# encoding: utf-8
import json
import rpyc

from flask import Flask, request
app = Flask(__name__)
# Create a RPyC connection to the remote ev3dev device.
# Use the hostname or IP address of the ev3dev device.
# If this fails, verify your IP connectivty via ``ping X.X.X.X``
conn = rpyc.classic.connect('192.168.0.160')

# import ev3dev2 on the remote ev3dev device
ev3dev2_motor = conn.modules['ev3dev2.motor']
ev3dev2_sensor = conn.modules['ev3dev2.sensor']
ev3dev2_sensor_lego = conn.modules['ev3dev2.sensor.lego']

addresses = ['outA', 'outB', 'outC', 'outD'] 
motor_types = ['large', 'medium']

# Get connected motor devices 
# Querying all the ports to verify if a motor is connected
@app.route('/api/motors', methods=['GET'])
def motors():
    data = {}
    
    for motor_type in motor_types:
        for address in addresses:
            if motor_type == 'large':
                try:
                    ev3dev2_motor.LargeMotor(address)
                    data[address] = 'large'
                except:
                   print('No %s motor connected on port %s'  % (motor_type, address))
            elif motor_type == 'medium':
                try:
                    ev3dev2_motor.MediumMotor(address)
                    data[address] = 'medium'
                except:
                   print('No %s motor connected on port %s' % (motor_type, address))
    return json.dumps(data)

# Get motor details
@app.route('/api/motors/<string:address>', methods=['GET'])
def motorDetails(address):
    motor = ev3dev2_motor.Motor(address)
    return json.dumps({'status': motor.state[0]})

# Move a motor 
# Provide a correct port
@app.route('/api/motors/<string:address>', methods=['POST'])
def movementMotor(address):
    req_data = request.get_json()

    #Parse request body data    
    polarity = req_data["polarity"]
    speed = req_data["speed"]
    rotations = req_data["rotations"]

    #Set motor instance motor 
    motor = ev3dev2_motor.Motor(address)
    motor.polarity = polarity
    motor.on_for_rotations(ev3dev2_motor.SpeedRPM(speed), rotations)
    motor.stop()

    return json.dumps({'status': motor.address})

app.run()

