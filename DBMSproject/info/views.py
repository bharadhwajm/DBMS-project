from django.shortcuts import render,redirect,HttpResponse
import sqlite3

def details(request,flight_no):
    connector=sqlite3.connect("airport.db")
    cursor=connector.cursor()

    result_crew=cursor.execute("select sname,position from cabin_crew where flight_no='{}'".format(flight_no))
    data_crew=result_crew.fetchall()

    result_grd=cursor.execute("select g.ename,g.desg from grd_staff g,flight f where f.uno=g.uno and f.flight_no='{}'".format(flight_no))
    data_grd=result_grd.fetchall()

    result_passengers=cursor.execute("select pid,pname,seat_no from passengers where flight_no='{}'".format(flight_no))
    data_passengers=result_passengers.fetchall()

    connector.close()
    
    return render(request,'choice.html',{'data_crew':data_crew,'data_grd':data_grd,'data_passengers':data_passengers})

# Create your views here.
def flightDetails(request,user):
    connector=sqlite3.connect("airport.db")
    cursor=connector.cursor()
    result=cursor.execute("select flight_no,arr_city,arr_time from flight where dep_city='Chennai'")
    data_dep=result.fetchall()
    result=cursor.execute("select flight_no,dep_city,arr_time from flight where arr_city='Chennai'")
    data_arr=result.fetchall()
    return render(request,'flightschedule.html',{'data_dep':data_dep,'data_arr':data_arr,'user':user})

from django.contrib import messages

def insertcabincrew(request):
    if request.method == "POST":
        staff_id = request.POST['sid']
        sname = request.POST['sname']
        flight_no = request.POST['flightno']
        position = request.POST['position']
        salary = request.POST['salary']
        dob = request.POST['dob']
        gender = request.POST['gender']

        connector = sqlite3.connect("airport.db")
        cursor = connector.cursor()

        # Check if the flight number exists in the flight table
        cursor.execute("SELECT COUNT(*) FROM flight WHERE flight_no = ?", (flight_no,))
        if cursor.fetchone()[0] == 0:
            connector.close()
            messages.error(request, "Invalid flight number", extra_tags='cabincrew')
            return redirect('insertcrew')

        # Insert the new cabin crew member
        cursor.execute("""
            INSERT INTO cabin_crew (staff_id, sname, flight_no, position, salary, dob, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (staff_id, sname, flight_no, position, salary, dob, gender))

        connector.commit()
        connector.close()
        messages.success(request, "Cabin crew member successfully inserted", extra_tags='cabincrew')
        return redirect('insertcrew')

    return render(request, 'newcabinstaff.html')


def insertemp(request):
    if request.method == "POST":
        eno = request.POST['empno']
        ename = request.POST['empname']
        desg = request.POST['designation']
        uno = request.POST['unitno']

        connector = sqlite3.connect("airport.db")
        cursor = connector.cursor()

        # Check if the unit number exists in the grd_unit table
        cursor.execute("SELECT COUNT(*) FROM grd_unit WHERE uno = ?", (uno,))
        if cursor.fetchone()[0] == 0:
            connector.close()
            messages.error(request, "Unit is not present", extra_tags='groundstaff')
            return redirect('insertgrdemp')

        # Insert the new ground staff member
        cursor.execute("""
            INSERT INTO grd_staff (eno, ename, desg, uno)
            VALUES (?, ?, ?, ?)
        """, (eno, ename, desg, uno))

        connector.commit()
        connector.close()
        messages.success(request, "Ground staff member successfully inserted", extra_tags='groundstaff')
        return redirect('insertgrdemp')

    return render(request, 'insertgrdemp')

def insertcrew(request):
    return render(request,'newcabinstaff.html')

def insertgrdemp(request):
    return render(request,'newgrdstaff.html')