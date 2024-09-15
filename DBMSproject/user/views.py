from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import sqlite3

# Create your views here.
def login(request):
    if request.method=="POST":
        flag=0
        empID=request.POST["username"]
        if empID.isnumeric()==False:
            flag=1
            return render(request,'login.html',{"flag":flag})
        inPassword=request.POST["password"]
        connector=sqlite3.connect('airport.db')
        cursor=connector.cursor()
        result=cursor.execute("select password from login where id={}".format(empID))
        password=result.fetchone()
        if password!=None:
            if inPassword==password[0]:
                return HttpResponseRedirect(reverse('flightDetails',args=[empID]))
        flag=1
        return render(request,'login.html',{"flag":flag})
    else:
        return render(request,'login.html')