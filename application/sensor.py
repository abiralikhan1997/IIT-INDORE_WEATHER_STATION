#from sense_hat import SenseHat
from datetime import datetime
from csv import DictReader, DictWriter
import os
import serial
import time
import pandas as pd
from random import random


class sensor_info:
	
	def __init__(self):
		self.current_date = datetime.now().strftime("%d-%m-%Y")
		self.filename = "data/" + self.current_date + ".csv"
		if not os.path.isfile(self.filename):
			self.f = open(self.filename, "w", newline="")
			self.writer = DictWriter(self.f, fieldnames=["Time", "Temperature", "Humidity", "Pressure", "Pm2.5", "Pm10"])
			self.writer.writeheader()
			self.f.close()

	## FOR NOVA SDS011 data collection.
	def sds011(self):
		#ser = serial.Serial('/dev/ttyUSB0')
		#data = []
		#for index in range(0,10):
		#	datum = ser.read()
		#	print(datum)
		#	data.append(datum)
		
		pm25 =  round(random()*100, ndigits=2)    #int.from_bytes(b''.join(data[2:4]),byteorder='little') / 10   #  round(random()*100, ndigits=2)    #
		pm10 =  round(random()*100, ndigits=2)    #int.from_bytes(b''.join(data[4:6]),byteorder='little') / 10  
		if pm25 and pm10:
			return pm25, pm10
		else:
			return None, None

	## FOR SENSEHAT data collection.
	def temp_humidty(self):
		#sense = SenseHat()
		airq= self.sds011()
		pm25=airq[0]
		pm10=airq[1]
		humidity = round(random()*100, ndigits=2)    #round(sense.get_humidity(), ndigits=2)     #
		temperature = round(random()*100, ndigits=2)    #round(sense.get_temperature(), ndigits=2)
		pressure = round(random()*100, ndigits=2)    #round(sense.get_pressure(), ndigits=2)
		if humidity and temperature:
			return humidity, temperature, pressure, pm25, pm10
		else:
			return None, None, None, None, None


	def write_logger(self, data):
		sds011_data = self.sds011()
		humidity = data[0]
		temperature = data[1]
		pressure = data[2]
		pm25 = sds011_data[0]
		pm10 = sds011_data[1]
		self.f = open(self.filename, "a", newline="")
		self.writer = DictWriter(self.f, fieldnames=["Time", "Temperature", "Humidity", "Pressure", "Pm2.5", "Pm10"])
		self.writer.writerow({
			"Time": datetime.now().strftime("%H:%M:%S"),
			"Temperature": temperature,
			"Pressure": pressure,
			"Humidity": humidity,
			"Pm2.5": pm25,
			"Pm10": pm10
			})
		self.f.close()
		time.sleep(20) ########--------------------------------------------------------------------------------> TO SET THE DATA SAMPLING TIME --- (20)

	def logger(self):    
		## for data logging loop
		while True:  
			#time.sleep(2)
			data = self.temp_humidty()
			if not any(data):
				continue
			present_date = datetime.now().strftime("%d-%m-%Y")
			if self.current_date != present_date:
				self.current_date = present_date
				self.filename = "data/" + self.current_date + ".csv"
				self.f = open(self.filename, "a+", newline="")
				self.writer = DictWriter(self.f, fieldnames=["Time", "Temperature", "Humidity", "Pressure", "Pm2.5", "Pm10"])
				self.writer.writeheader()
				self.f.close()
			self.write_logger(data)


	## TO get the data history.
	def get_time_data(self, filename):
		exists = os.path.isfile("data/"+filename)
		if exists:
			data = pd.read_csv("data/"+filename)
			return data.to_dict("records")
		else:
			data = pd.read_csv("application/static/"+"No_data.csv")
			return data.to_dict("records")
		return None

	## TO get the plot data.
	def get_data_plot(self, filename):

		exists = os.path.isfile("data/"+filename)
		if exists:
			
			csv_data = pd.read_csv("data/"+filename)
			time_data = csv_data['Time'].tolist()
			temp_data = csv_data['Temperature'].tolist()
			humi_data = csv_data['Humidity'].tolist()
			press_data = csv_data['Pressure'].tolist()
			pm25_data = csv_data['Pm2.5'].tolist()
			pm10_data = csv_data['Pm10'].tolist()

			return time_data, temp_data, humi_data, press_data, pm25_data, pm10_data

		else:
			data = pd.read_csv("static/"+"No_data.csv")
			return data.to_dict("records")
		return None


	## TO get the average temp, humidity, pressure, airQuality of the current day
	def average(self, filename):

		def avg(data_list):
			total=0
			for value in data_list:
				total = total + value
			data_avg = round(total/len(data_list), ndigits=2)
			return data_avg

		exists = os.path.isfile("data/"+ filename)
		if exists:
			csv_data = pd.read_csv("data/"+ filename)
			temp_data = csv_data['Temperature'].tolist()
			humi_data = csv_data['Humidity'].tolist()
			press_data = csv_data['Pressure'].tolist()
			pm25_data = csv_data['Pm2.5'].tolist()
			pm10_data = csv_data['Pm10'].tolist()
		else:
			return None
		
		return avg(temp_data), avg(humi_data), avg(press_data), avg(pm25_data), avg(pm10_data)
