
from application import app, sensor_func
from flask import request, render_template, make_response, jsonify
from datetime import datetime
from threading import Thread
import os


def log_thread():
	thread = Thread(target=sensor_func.logger)
	thread.start()
	return os.getpid()



### Page1--------------------------------------------FRONT PAGE
@app.route("/")
def hello():    
    return render_template("welcome_page.html")

### Welcome Page real time data routing app-------------
@app.route("/real_time")
def lab_temp():
    data = sensor_func.temp_humidty()
    data = {
    "Time":str(datetime.now().strftime("%H:%M:%S")),
    "Temperature": str(data[1]),
    "Humidity": str(data[0]),
    "Pressure": str(data[2]),
    "Pm25": str(data[3]),
    "Pm10": str(data[4])
    }
    resp = make_response(data, 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

########## Welcome Page avarage data routing app-------------
@app.route("/get_avg_value_realtime", methods=["GET","POST"])
def avg_value():
    form_data ={'date': str(datetime.now().strftime("%d-%m-%Y"))}
    all_avg = sensor_func.average(filename=form_data["date"]+".csv")
    data = {
        "temperature":all_avg[0],
        "humidity":all_avg[1],
        "pressure":all_avg[2],
        "pm25":all_avg[3],
        "pm10":all_avg[4]
    }
    resp = make_response(jsonify(data), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp





### Page2----------------------------------------------DATABASE
@app.route("/show_logs", methods=["GET", "POST"])
def show_logs():
    if request.method == "GET":
        return render_template("database1.html")

### dataBase Page data database routing app------------
@app.route("/get_logdata", methods=["POST"])
def get_logdata():
    form_data = request.form.to_dict()
    all_logs = sensor_func.get_time_data(filename=form_data["date"]+".csv")
    resp = make_response(jsonify(all_logs), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

### dataBase Page data database plot routing app------------
@app.route("/get_logdata_for_plot",methods=["GET", "POST"])
def get_logdata_for_ploting():
    form_data =request.form.to_dict()   #{'date': '27-09-2021'}#
    all_plots = sensor_func.get_data_plot(filename=form_data["date"]+".csv")
    data = {
        "time":all_plots[0],
        "temperature":all_plots[1],
        "humidity":all_plots[2],
        "pressure":all_plots[3],
        "pm25":all_plots[4],
        "pm10":all_plots[5]
    }
    resp = make_response(jsonify(data), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

########## dataBase Page avarage data routing app-------------

