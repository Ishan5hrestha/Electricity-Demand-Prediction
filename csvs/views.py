from django.shortcuts import render
from .cs import interpollable,averager,cubic_spline
from .forms import CsvModuleForm
from .models import Csv
from adminpanel.models import data,tdataall,rdata,hdata
import csv
import mysql.connector
from adminpanel.date_converter import adtobs,bsbaarfinder
from adminpanel.dbmaster import db_reader_hourly,db_reader
from copy import deepcopy
# Create your views here.
edataxaxis= [1,2,3,4,5,6,6.5,7,7.5,8,9,10,11,12,13,14,15,16,17,17.5,18,18.5,19,19.5,20,21,22,23,24]
hdataxaxis=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
tdataxaxis=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

def edata_uploader(obj,reader,intornot):
    alldata = []
    for i, row in enumerate(reader):
        eutarow = []
        if i == 0 and float(row[24]) > 10:
            pass
        else:
            for item in row:
                eutarow.append(float(item))
            alldata.append(eutarow)
            # print(f"t{i} : {type(eutarow)}")
    # print(f"alldata: {alldata}")

    if intornot != None:
        ipdata = []
        for i in range(len(alldata)):
            # print(f"{i} : {interpollable(alldata[i])}")
            if not interpollable(alldata[i]):
                # print("avereager ma xire")
                try:
                    alldata[i] = averager(alldata[i - 1], alldata[i], alldata[i + 1])
                except:
                    alldata[i] = averager(alldata[i - 1], alldata[i], alldata[i-1])
            # print("cubic spline gaarnalgaao")
            ipdata.append(cubic_spline(edataxaxis,alldata[i]))
            # print(ipdata)
        # print(f"datalen : {len(ipdata)}")
        # print(f"rowlen : {len(ipdata[1])}")
        # print
    else:
        ipdata = alldata

    for i in range(len(ipdata)):
        row = ipdata[i]
        data.objects.create(
            hr0100=row[0],
            hr0200=row[1],
            hr0300=row[2],
            hr0400=row[3],
            hr0500=row[4],
            hr0600=row[5],
            hr0630=row[6],
            hr0700=row[7],
            hr0730=row[8],
            hr0800=row[9],
            hr0900=row[10],
            hr1000=row[11],
            hr1100=row[12],
            hr1200=row[13],
            hr1300=row[14],
            hr1400=row[15],
            hr1500=row[16],
            hr1600=row[17],
            hr1700=row[18],
            hr1730=row[19],
            hr1800=row[20],
            hr1850=row[21],
            hr1900=row[22],
            hr1950=row[23],
            hr2000=row[24],
            hr2100=row[25],
            hr2200=row[26],
            hr2300=row[27],
            hr2400=row[28]
        )
    obj.activated = True
    obj.save()

def tdata_uploader(obj,reader,intornot):
    alldata = []
    ekrow = [0.0]*24
    syear = 0
    smonth = 0
    sdate = 0
    stime = -1
    mdate = 0
    datadate = 1    #check if dataa is consistent or gap in data
    for i, row in enumerate(reader):
        if i == 0 and isinstance(row[2],str):
            continue

        descstring = row[0].split(" ")
        mdatey = descstring[0].split("/")
        myear = int(mdatey[2])
        mmonth = int(mdatey[0])
        mdate = int(mdatey[1])
        mtime = int(descstring[1])
        mvalue = round(float(row[3]), 2)
        baar = 0
        khaliraixa= False
        gate = []
        gate = adtobs(myear, mmonth, mdate)
        # print(gate[0])
        myear = gate[0]
        mmonth = gate[1]
        mdate = gate[2]
        if abs(mdate-sdate)>1 and mdate!=1:
            khaliraixa = True
        if myear==syear and mmonth==smonth and mdate==sdate:
            #print("if")
            ekrow[mtime]=mvalue
        elif syear==0 or smonth==0 or sdate==0:
            #print("elif")
            ekrow[mtime]=mvalue
        else:
            #print("else")
            gate[0] = syear
            gate[1] = smonth
            gate[2] = sdate
            gate.pop(3)
            gate.extend(ekrow)
            alldata.append(gate)
            if khaliraixa:alldata.append([myear,mmonth,mdate-1]+[0.0]*24)
            ekrow = [0.0]*24
            ekrow[mtime]=mvalue
        syear = myear
        smonth = mmonth
        sdate = mdate
        stime = mtime
        print(f"gate{gate} mtimr {mtime} ekrow {ekrow}")
    # last ko date liyena j gardani tsaile yei haldeko last date
    gate[0] = syear
    gate[1] = smonth
    gate[2] = sdate
    gate.pop(3)
    gate.extend(ekrow)
    alldata.append(gate)
    print("yoho alldata",alldata)

    if intornot != None:
        rough = deepcopy(alldata)
        #print(f"rough {rough}")
        for i in alldata:
            i.pop(2)
            i.pop(1)
            i.pop(0)
        #print(f"popped adata {alldata}")
        #print(f"rough {rough}")

        ipdata = []
        for i in range(len(alldata)):
            if not interpollable(alldata[i]):
                print("avereager ma xire")
                try:
                    alldata[i] = averager(alldata[i - 1], alldata[i], alldata[i + 1])
                except:
                    alldata[i] = averager(alldata[i - 1], alldata[i], alldata[i-1])
            # print("cubic spline gaarnalgaao")
            ipdata.append(cubic_spline(tdataxaxis,alldata[i]))
            # print(ipdata)

        #print("interpolation ta rammari garyo")
        j=0
        alldata = []
        for i in rough:
            gate = [0,0,0]
            gate[0] = i[0]
            gate[1] = i[1]
            gate[2] = i[2]
            gate.extend(ipdata[j])
            alldata.append(gate)
            j+=1
        #print("ipdata")

    ipdata = alldata
    #print(ipdata)

    for i in range(len(ipdata)):
        row = ipdata[i]
        #print("object banauna xiro")
        tdataall.objects.create(
            year=row[0],
            month=row[1],
            day=row[2],
            hr0000=row[3],
            hr0100=row[4],
            hr0200=row[5],
            hr0300=row[6],
            hr0400=row[7],
            hr0500=row[8],
            hr0600=row[9],
            hr0700=row[10],
            hr0800=row[11],
            hr0900=row[12],
            hr1000=row[13],
            hr1100=row[14],
            hr1200=row[15],
            hr1300=row[16],
            hr1400=row[17],
            hr1500=row[18],
            hr1600=row[19],
            hr1700=row[20],
            hr1800=row[21],
            hr1900=row[22],
            hr2000=row[23],
            hr2100=row[24],
            hr2200=row[25],
            hr2300=row[26]
        )
    obj.activated = True
    #print("activatee garera save ni gare")
    obj.save()


def rdata_uploader(obj,reader,intornot):
    alldata = []
    ekrow = [0.0]*33        #besi vayeni faraak pardaina kinaki rakhda count garerai rakhekoxu
    syear = 0
    smonth = 0
    sdate = 0
    stime = -1
    datadate = 1    #check if dataa is consistent or gap in data
    for i, row in enumerate(reader):
        if i == 0 and isinstance(row[2],str):
            continue
        myear = int(row[4])
        mmonth = int(row[5])
        mdate = int(row[6])
        mvalue = round(float(row[7]),2)
        gate = []
        gate = adtobs(myear,mmonth,mdate)
        #print(gate[0])
        myear = gate[0]
        mmonth = gate[1]
        mdate = gate[2]
        if myear==syear and mmonth==smonth:
            #print("if")
            ekrow[mdate-1]=mvalue
        elif syear==0 or smonth==0:
            #print("elif")
            ekrow[mdate-1]=mvalue
        else:
            #print("else")
            gate[0] = syear
            gate[1] = smonth
            gate[2] = sdate
            gate.pop(3)
            gate.pop(2)
            gate.extend(ekrow)
            alldata.append(gate)
            ekrow = [0.0]*33
            ekrow[mdate-1]=mvalue
        syear = myear
        smonth = mmonth
        sdate = mdate
        #print(f"gate{gate} mdate {mdate} ekrow {ekrow}")
    # last ko date liyena j gardani tsaile yei haldeko last date
    gate[0] = syear
    gate[1] = smonth
    gate[2] = sdate
    gate.pop(3)
    gate.pop(2)
    gate.extend(ekrow)
    alldata.append(gate)

    print(alldata)
    print(f"length {len(alldata)}")
    print(f"length {len(alldata[10])}")

    for i in range(len(alldata)):
        row = alldata[i]
        #print("object banauna xiro")
        rdata.objects.create(
            year=row[0],
            month=row[1],
            rd1 = row[2],
            rd2 = row[3],
            rd3 = row[4],
            rd4 = row[5],
            rd5 = row[6],
            rd6 = row[7],
            rd7 = row[8],
            rd8 = row[9],
            rd9 = row[10],
            rd10 = row[11],
            rd11 = row[12],
            rd12 = row[13],
            rd13 = row[14],
            rd14 = row[15],
            rd15 = row[16],
            rd16 = row[17],
            rd17 = row[18],
            rd18 = row[19],
            rd19 = row[20],
            rd20 = row[21],
            rd21 = row[22],
            rd22 = row[23],
            rd23 = row[24],
            rd24 = row[25],
            rd25 = row[26],
            rd26 = row[27],
            rd27 = row[28],
            rd28 = row[29],
            rd29 = row[30],
            rd30 = row[31],
            rd31 = row[32],
            rd32 = row[33]
        )
    obj.activated = True
    #print("activatee garera save ni gare")
    obj.save()


def hdata_uploader(obj,reader,intornot):
    alldata = []
    ekrow = [0.0] * 24
    syear = 0
    smonth = 0
    sdate = 0
    stime = -1
    datadate = 1  # check if dataa is consistent or gap in data
    for i, row in enumerate(reader):
        if i == 0 and isinstance(row[2], str):
            continue

        myear = int(row[4])
        mmonth = int(row[5])
        mdate = int(row[6])
        mtime = int(row[7])
        mvalue = round(float(row[8]), 1)
        baar = 0
        gate = []
        gate = adtobs(myear, mmonth, mdate)
        # print(gate[0])
        myear = gate[0]
        mmonth = gate[1]
        mdate = gate[2]
        if myear == syear and mmonth == smonth and mdate == sdate:
            #print("if")
            ekrow[mtime-3] = mvalue
        elif syear == 0 or smonth == 0 or sdate == 0:
            #print("elif")
            ekrow[mtime-3] = mvalue
        else:
            #print("else")
            gate[0] = syear
            gate[1] = smonth
            gate[2] = sdate
            gate.pop(3)
            gate.extend(ekrow)
            gate.extend([0.0])
            alldata.append(gate)
            ekrow = [0.0] * 24
            ekrow[mtime-3] = mvalue
        syear = myear
        smonth = mmonth
        sdate = mdate
        stime = mtime
        #print(f"gate{gate} mtimr {mtime} ekrow {ekrow}")
    # last ko date liyena j gardani tsaile yei haldeko last date
    gate[0] = syear
    gate[1] = smonth
    gate[2] = sdate
    gate.pop(3)
    gate.extend(ekrow)
    gate.extend([0.0])
    alldata.append(gate)

    #print(alldata)
    #print(f"length {len(alldata)}")
    #print(f"length {len(alldata[10])}")

    if intornot != None:
        rough = deepcopy(alldata)
        #print(f"rough {rough}")
        for i in alldata:
            i.pop(2)
            i.pop(1)
            i.pop(0)
        #print(f"popped adata {alldata}")
        x = 0       # last koma vaalue dina. hawa vaalue dine ho tara. suru ko lai lastma haldine
        for i in range(len(alldata)-1):
            alldata[i][24] = alldata[i+1][0]
            print(alldata)
            x += 1
        alldata[x][24] = alldata[x][0]

        #print(f"rough {rough}")

        ipdata = []
        #print("interpolate gareko")
        for i in range(len(alldata)):
            ruff = cubic_spline(hdataxaxis, alldata[i])
            #print(ruff)
            ruff.pop(24)
            ipdata.append(ruff)
        #print(ipdata)

        #print("interpolation ta rammari garyo")
        j = 0
        alldata = []
        for i in rough:
            gate = [0, 0, 0]
            gate[0] = i[0]
            gate[1] = i[1]
            gate[2] = i[2]
            print(gate)
            print(ipdata[j])
            gate.extend(ipdata[j])
            print(gate)
            alldata.append(gate)
            j += 1
        #print("ipdata")

    ipdata = alldata
    #print("ipdata",ipdata)

    for i in range(len(ipdata)):
        row = ipdata[i]
        print("row",row)
        print("object banauna xiro")
        hdata.objects.create(
            year = row[0],
            month = row[1],
            day = row[2],
            hr0900 = row[3],
            hr1000 = row[4],
            hr1100 = row[5],
            hr1200 = row[6],
            hr1300 = row[7],
            hr1400 = row[8],
            hr1500 = row[9],
            hr1600 = row[10],
            hr1700 = row[11],
            hr1800 = row[12],
            hr1900 = row[13],
            hr2000 = row[14],
            hr2100 = row[15],
            hr2200 = row[16],
            hr2300 = row[17],
            hr0000 = row[18],
            hr0100 = row[19],
            hr0200 = row[20],
            hr0300 = row[21],
            hr0400 = row[22],
            hr0500 = row[23],
            hr0600 = row[24],
            hr0700 = row[25],
            hr0800 = row[26]
        )
        print("object baano")
    obj.activated = True
    print("activatee garera save ni gare")
    obj.save()

def upload_file_view(request):
    try:
        con1 = mysql.connector.connect(host="localhost", user="root", passwd="", database="neadata")
        cursor1 = con1.cursor()

        form = CsvModuleForm(request.POST or None, request.FILES or None)
        year = request.POST.get('year')
        month = request.POST.get('month')
        intornot = request.POST.get('intornot')
        #print(f"intornot : {intornot}")
        datatype = request.POST.get('type')
        if datatype =="edata": dbname = "y" + str(year) + str(month)

        #print("valid vayena")
        if form.is_valid():
            #print("valid vayo")
            form.save()
            form = CsvModuleForm()
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path,'r') as f:
                reader = csv.reader(f)

                # put dataa in list and make it float
                if datatype == "edata":
                    edata_uploader(obj, reader, intornot)
                    sqlcommand1 = "CREATE TABLE %s LIKE adminpanel_data;" % (dbname)
                    cursor1.execute(sqlcommand1)
                    sqlcommand1 = "INSERT INTO %s SELECT * FROM adminpanel_data;" % (dbname)
                    cursor1.execute(sqlcommand1)
                    sqlcommand1 = "TRUNCATE TABLE adminpanel_data;"
                    cursor1.execute(sqlcommand1)
                    sqlcommand1 = "TRUNCATE TABLE csvs_csv;"  # only kept to debug interpolation process works fine once interpolation is done
                    cursor1.execute(sqlcommand1)
                    return render(request, "upload.html", {'form': form, 'successful': True})

                if datatype == "tdata":
                    tdata_uploader(obj, reader, intornot)
                    sqlcommand1 = "TRUNCATE TABLE csvs_csv;"  # only kept to debug interpolation process works fine once interpolation is done
                    cursor1.execute(sqlcommand1)
                    return render(request, "upload.html", {'form': form, 'successful': True})

                if datatype == "rdata":
                    rdata_uploader(obj, reader, intornot)
                    sqlcommand1 = "TRUNCATE TABLE csvs_csv;"  # only kept to debug interpolation process works fine once interpolation is done
                    cursor1.execute(sqlcommand1)
                    return render(request, "upload.html", {'form': form, 'successful': True})

                if datatype == "hdata":
                    hdata_uploader(obj, reader, intornot)
                    sqlcommand1 = "TRUNCATE TABLE csvs_csv;"  # only kept to debug interpolation process works fine once interpolation is done
                    cursor1.execute(sqlcommand1)
                    return render(request, "upload.html", {'form': form, 'successful': True})

        return render(request,"upload.html",{'form':form})
    except:
        error = True
        sqlcommand1 = "TRUNCATE TABLE adminpanel_data;"
        cursor1.execute(sqlcommand1)                #remove when interpolation error is doone
        sqlcommand1 = "TRUNCATE TABLE csvs_csv;"    #only kept to debug interpolation process works fine once interpolation is done
        cursor1.execute(sqlcommand1)
        return render(request, "upload.html", {'form': form,'error':error})