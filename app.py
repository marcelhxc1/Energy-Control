from flask import Flask, request, jsonify
import time
from ina219 import INA219
import base64

app = Flask(__name__)

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

hourly_readings = []
daily_readings = []
weekly_readings = []
monthly_readings = []

@app.route('/power', methods=['GET'])
def get_power():
    token = request.args.get('token')
    # Decode the string
    decoded_string = base64.b64decode(token).decode('utf-8')
    # Split the string into client_id and client_secret
    client_id, client_secret = decoded_string.split(':')

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        return jsonify(error='Unauthorized'), 401

    #if request.args.get('client_id') != CLIENT_ID or request.args.get('client_secret') != CLIENT_SECRET:
    #    return jsonify(error='Unauthorized'), 401
    return jsonify(power=read_power())

def read_power():
    power = ina.power()
    current_time = int(time.time())
    hourly_readings.append((current_time, power))
    daily_readings.append((current_time, power))
    weekly_readings.append((current_time, power))
    monthly_readings.append((current_time, power))
    return power

@app.route('/weekly_power', methods=['GET'])
@auth_required
def get_weekly_power():
    try:
        current_time = int(time.time())
        weekly_power = 0
        for reading in weekly_readings:
            if current_time - reading[0] <= 604800:
                weekly_power += reading[1]
        return weekly_power
    except:
        return jsonify({'error': 'Unable to retrieve weekly power consumption data'}), 500

@app.route('/hourly_power', methods=['GET'])
@auth_required
def get_hourly_power():
    try:
        current_time = int(time.time())
        hourly_power = 0
        for reading in hourly_readings:
            if current_time - reading[0] <= 3600:
                hourly_power += reading[1]
        return hourly_power
    except:
        return jsonify({'error': 'Unable to retrieve weekly power consumption data'}), 500

@app.route('/daily_power', methods=['GET'])
@auth_required
def get_daily_power():
    try:
        current_time = int(time.time())
        daily_power = 0
        for reading in daily_readings:
            if current_time - reading[0] <= 86400:
                daily_power += reading[1]
        return daily_power
    except:
        return jsonify({'error': 'Unable to retrieve daily power consumption data'}), 500

@app.route('/montly_power', methods=['GET'])
@auth_required
def get_monthly_power():
    try:
        current_time = int(time.time())
        monthly_power = 0
        for reading in monthly_readings:
            if current_time - reading[0] <= 2592000:
                monthly_power += reading[1]
        return monthly_power
    except:
        return jsonify({'error': 'Unable to retrieve montly power consumption data'}), 500


if __name__ == '__main__':
    app.run()
# to access : `http://localhost:5000/power?token=base64token fix