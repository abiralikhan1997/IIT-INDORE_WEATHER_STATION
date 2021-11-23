from application import app,routes,os,signal


if __name__ == '__main__' :
	try:
		pid = routes.log_thread()
		app.run(
			host='192.168.0.194',  
			threaded=True,
            debug=False			
			)
	except:
		print("Stopping the logger...")
	finally:
		os.kill(pid, signal.SIGTERM)