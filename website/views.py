from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Ipdevices
from .models import db
import json, os, sys, re, socket, datetime, time

FILE = os.path.join(os.getcwd(), "networkinfo.log")

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully', category='success')
    return jsonify({})
    #return render_template("note.html", user=current_user)  


@views.route('/note', methods=['GET', 'POST'])
@login_required
def note_add():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("note.html", user=current_user)


@views.route('/ipDevices', methods =['GET', 'POST'])
@login_required
def ipDevices_status():
    if request.method == 'POST':
        ipAddr = request.form.get('ipAddress')
        ipNam = request.form.get('ipName')
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        ipexist = Ipdevices.query.filter_by(ipaddress =ipAddr).first()

        if(re.search(regex, ipAddr)==None): 
            flash('You have entered an Invalid ip address', category='error')
        elif ipexist:
            flash('IP Address alreaddy exist', category='error')
        elif len(ipAddr) ==0:
            flash('IP addresss can not be empty', category='error')
        elif len(ipNam) == 0:
            flash('IP Address name cannot be empty', category='error')
        else:
            new_ip =Ipdevices(ipaddress =ipAddr, ipname =ipNam, ipstatus = ipNam)
            db.session.add(new_ip)
            db.session.commit()
            flash('IP Devices successfully added', category='success')
   
    data_ip = Ipdevices.query.all()
    status=''
    #for ip in data_ip:
    #    ip1 = ip.ipaddress
    #    responce = os.popen("ping " + ip1).read()
    #    if 'Received = 4' in responce:
    #        status = 'Online'
    #    else:
    #        status='Offline' 
    return render_template('devices.html', user=current_user, data_ip= data_ip ,status=status)



@views.route('/delete-ip-device', methods =['POST'])
def delete_ip_device():
    ipaddr = json.loads(request.data)
    idaddrID = ipaddr['ipId']
    ipaddre = Ipdevices.query.get(idaddrID)
    if ipaddre:
        db.session.delete(ipaddre)
        db.session.commit()
        flash('IP Device deleted successfully', category='success')
    return jsonify({})


              
def ping():
	# to ping a particular IP
	try:
		socket.setdefaulttimeout(3)
		
		# if data interruption occurs for 3
		# seconds, <except> part will be executed
			
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# AF_INET: address family
		# SOCK_STREAM: type for TCP

		host = "8.8.8.8"
		port = 53

		server_address = (host, port)
		s.connect(server_address)

	except OSError as error:
		return False
		# function returns false value
		# after data interruption

	else:
		s.close()
		# closing the connection after the
		# communication with the server is completed
		return True


def calculate_time(start, stop):

	# calculating unavailability
	# time and converting it in seconds
	difference = stop - start
	seconds = float(str(difference.total_seconds()))
	return str(datetime.timedelta(seconds=seconds)).split(".")[0]


@views.route('/google_server', methods=['GET','POST'])
@login_required
def server_connectivity():
    if 1==1:
        # main function to call functions
        monitor_start_time = datetime.datetime.now()
        monitoring_date_time = "monitoring started at: " + \
            str(monitor_start_time).split(".")[0]

        if ping():
            # if true
            # if ping returns true
            live = "\nCONNECTION ACQUIRED\n"
            #print(live)
            connection_acquired_time = datetime.datetime.now()
            acquiring_message = "connection acquired at: " + \
                str(connection_acquired_time).split(".")[0]
            #print(acquiring_message)

            with open(FILE, "a") as file:
            
                # writes into the log file
                file.write(live)
                file.write(acquiring_message)
            monitoring_date_time =monitoring_date_time
            # monitoring will only start when
            # the connection will be acquired

        else:
            not_live = "\nCONNECTION NOT ACQUIRED\n"
            #print(not_live)

            with open(FILE, "a") as file:
            
                # writes into the log file
                file.write(not_live)
            # if false
            while True:
            
                # infinite loop to see if the connection is acquired
                if not ping():
                    
                    # if connection not acquired
                    time.sleep(1)
                else:
                    
                    # if connection is acquired
                    if ping():
		                # if ping returns true
                        live = "\nCONNECTION ACQUIRED\n"
                        #print(live)
                        connection_acquired_time = datetime.datetime.now()
                        acquiring_message = "connection acquired at: " + \
                            str(connection_acquired_time).split(".")[0]
                        #print(acquiring_message)

                        with open(FILE, "a") as file:
                        
                            # writes into the log file
                            file.write(live)
                            file.write(acquiring_message)

                        return True

                    else:
                        # if ping returns false
                        not_live = "\nCONNECTION NOT ACQUIRED\n"
                        #print(not_live)

                        with open(FILE, "a") as file:
                        
                            # writes into the log file
                            file.write(not_live)
                        return False

                monitoring_date_time=monitoring_date_time
                break

        with open(FILE, "a") as file:
        
            # write into the file as a into networkinfo.log,
            # "a" - append: opens file for appending,
            # creates the file if it does not exist???
            file.write("\n")
            file.write(monitoring_date_time + "\n")

        while True:
        
            # infinite loop, as we are monitoring
            # the network connection till the machine runs
            if ping():
                
                # if true: the loop will execute after every 5 seconds
                time.sleep(5)

            else:
                # if false: fail message will be displayed
                down_time = datetime.datetime.now()
                fail_msg = "disconnected at: " + str(down_time).split(".")[0]
                #print(fail_msg)

                with open(FILE, "a") as file:
                    # writes into the log file
                    file.write(fail_msg + "\n")

                while not ping():
                
                    # infinite loop, will run till ping() return true
                    time.sleep(1)

                up_time = datetime.datetime.now()
                
                # after loop breaks, conn ection restored
                uptime_message = "connected again: " + str(up_time).split(".")[0]

                down_time = calculate_time(down_time, up_time)
                unavailablity_time = "connection was unavailable for: " + down_time

                #print(uptime_message)
                #print(unavailablity_time)

                with open(FILE, "a") as file:
                    
                    # log entry for connection restoration time,
                    # and unavailability time
                    file.write(uptime_message + "\n")
                    file.write(unavailablity_time + "\n")
   
    
    render_template('servers.html',  user=current_user ,live= monitoring_date_time , not_live=not_live, file=file)
    server_connectivity()


@views.route('/serverConnection', methods=['GET','POST'])
def serverPage():
	
    return render_template('servers.html', user=current_user) 

@views.route('/base', methods=['GET','POST']
def base_home():

    return render_template('base.html', user=current_user) 



