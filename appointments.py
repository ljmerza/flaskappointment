#!/usr/bin/env python

from flask import Flask, send_from_directory, request
from sqlalchemy import create_engine
from json import dumps
from uuid import uuid1
from datetime import datetime

dbFile = r'appointments.sqlite'


# create sqlalchemy db table
e = create_engine('sqlite:///appointments.db')
conn = e.connect()
conn.execute("CREATE TABLE IF NOT EXISTS appointments (guid number, timedate number, description text)")


# create flask app
app = Flask(__name__, static_url_path='')




@app.route("/data", methods=['GET'])
def data():
	# parse request body and open db connection
	description = request.args.get('description')
	print(description)

	conn = e.connect()

	# if no argument then get all appointments
	if description == '':
		data = conn.execute("SELECT timedate, description FROM appointments")
	# else get specific data
	else:
		data = conn.execute("SELECT timedate, description FROM appointments WHERE description LIKE ?", '%'+description+'%')
	# convert sqlalchemy object to array of json data before responding to client
	return dumps([dict(r) for r in data])




@app.route('/new', methods=['POST'])
def new():
	description = request.form['description']
	time = request.form['time']
	date = request.form['date']

	# if any fields are blank then dont modify db
	if time == '' or date == '' or description == '':
		return app.send_static_file('index.html')

	try:
		timeDate = datetime.strptime(date+'-'+time, '%Y-%m-%d-%H:%M').timestamp()
	# if cant parse then return index file
	except OverflowError:
		return app.send_static_file('index.html')

	conn = e.connect()
	# insert data into db if all form data exists and time correctly parsed
	conn.execute("INSERT INTO appointments (guid, timedate, description) VALUES (?,?,?)", str(uuid1()), timeDate, description)

	# return index file
	return app.send_static_file('index.html')



# static file server routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)




if __name__ == '__main__':
    app.run(debug=True)