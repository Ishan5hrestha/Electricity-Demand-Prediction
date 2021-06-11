from django.shortcuts import render,redirect
from .dbmaster import db_reader,db_reader_hourly
from .models import User
import mysql.connector
from operator import itemgetter
from django.contrib import messages
from csvs.views import upload_file_view
import csv
from django.http import HttpResponse

# Create your views here.
def index(request):
    dataJSON = db_reader_hourly('y207401')
    return render(request,"dashboard.html",{'data':dataJSON})

def dashboard(request):
    dataJSON = db_reader_hourly('y207401')
    return render(request,"dashboard.html",{'data':dataJSON})

def calender(request):
    return render(request,"calender.html")

def datasets(request):
    if request.method == 'POST':
        datatype = request.POST['type']
        if datatype=='edata':
            year = request.POST['year']
            month = request.POST['month']
            tablename = "y"+year+month
            return render(request,"datasets.html",{"tabledata":db_reader_hourly(tablename),"datatype":datatype,"year":year,"month":month})
        if datatype=='tdata':
            return render(request, "datasets.html",{"tabledata": db_reader('adminpanel_tdataall',27), "datatype": datatype})
        if datatype=='rdata':
            return render(request, "datasets.html",{"tabledata": db_reader('adminpanel_rdata',34), "datatype": datatype})
        if datatype=='hdata':
            return render(request, "datasets.html",{"tabledata": db_reader('adminpanel_hdata',27), "datatype": datatype})

    return render(request,"datasets.html")


def forgot_password(request):
    return render(request,"forgot-password.html")

def login(request):
    con1 = mysql.connector.connect(host="localhost",user="root",passwd="",database="neadata")
    cursor1 = con1.cursor()
    con2 = mysql.connector.connect(host="localhost", user="root", passwd="", database="neadata")
    cursor2 = con2.cursor()
    con3 = mysql.connector.connect(host="localhost", user="root", passwd="", database="neadata")
    cursor3 = con3.cursor()
    sqlcommand1 = "select email from adminpanel_user"
    sqlcommand2 = "select password from adminpanel_user"
    sqlcommand3 = "select fname from adminpanel_user"
    cursor1.execute(sqlcommand1)
    cursor2.execute(sqlcommand2)
    cursor3.execute(sqlcommand3)
    e = []
    p = []
    n = []
    for i in cursor1:
        e.append(i)
    for j in cursor2:
        p.append(j)
    for k in cursor3:
        n.append(k)
    res1 = list(map(itemgetter(0),e))
    res2 = list(map(itemgetter(0),p))
    res3 = list(map(itemgetter(0),n))

    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        i=0
        k=len(res1)
        while i<k:
            if res1[i]==email and res2[i]==password:
                dataJSON = db_reader_hourly('y207401')
                return render(request,"dashboard.html",{'name':res3[i],'data':dataJSON})
                break
            i+=1;
        else:
            messages.info(request,"Check Username or Password")
            return render(request,"login.html",{'valid':False})
    return render(request,"login.html",{'valid':True})

def maps(request):
    return render(request,"maps.html")

def settings(request):
    return render(request,"settings.html")

def register(request):
    if request.method=="POST":
        user = User();
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.repassword = request.POST['repassword']
        if user.password != user.repassword:
            return redirect('register')
        elif user.fname=="" or user.password=="":
            messages.info(request,'Some fields are empty')
            return redirect('register')
        else:
            user.save()
            messages.info(request, 'User created, Please login.')
            return render(request, "register.html",{'usercreated':True})
    return render(request,"register.html")
