from flask import Flask
from application import sensor
import os
import signal


app = Flask(__name__)
sensor_func = sensor.sensor_info()



from application import routes
