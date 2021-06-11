from django.shortcuts import render,redirect
from adminpanel.dbmaster import db_reader,db_reader_hourly,db_table_exists
from adminpanel.date_converter import bsbaarfinder,bs_months
from .models import puredataset
import mysql.connector
import matplotlib.pyplot as plt 
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
import pickle


def search(data,year,month,day):
    for i in range(len(data)):
        if data[i][1]==year and data[i][2]==month and data[i][3]==day:
            #print("index: ",i)
            return i
    return 0
#   Edata anausaar time milaune
def time_milaune(type,i,j):
    #print(f"bi: {i} j: {j}")
    if type=="tdata":
        if j==26:
            i+=1
            j=4
        else:
            j += 2
        #print(f"ai: {i} j: {j}")
        return i,j
    if type=="hdata":
        if j<11:
            i-=1
            j=17+j
        elif j>=11:
            j = j-7
        else:
            j += 8
        #print(f"ai: {i} j: {j}")
        return i,j


def set_value(edata,tdata,hdata):
    result1 = []
    result2 = []
    result = []
    rough = []
    #print(edata)
    year = edata[0][0]
    month = edata[0][1]
    day = edata[0][2]
    #shortcut = True

    #   Temperature ma tyo data ka bata suruvakoxa
    tindex = search(tdata,year,month,day)

    #   Humidity ma tyo data ka bata suruvakoxa
    hindex = search(hdata,year,month,day)
    ti, tj = time_milaune("tdata", 0, 3)
    hi, hj = time_milaune("hdata", 0, 3)

    try:
        for i in range(len(edata)):
            #  Tdata
            for k in range(len(tdata)):
                if edata[i][0] == tdata[k][1] and edata[i][1] == tdata[k][2] and edata[i][2] == tdata[k][3]:
                    for l in range(4,28):
                            for x in range(3,27):
                                ti, tj = time_milaune("tdata",i,x)
                                result1.append([edata[i][0],edata[i][1],edata[i][2],bsbaarfinder(edata[i][0],edata[i][1],edata[i][2]),x-2,edata[i][x],tdata[tindex+ti][tj]])
                                print(edata[i][0],edata[i][1],edata[i][2],bsbaarfinder(edata[i][0],edata[i][1],edata[i][2]),x-2,edata[i][x],tdata[tindex+ti][tj])
                            break
    except:
        print(result1)
    try:
        for i in range(len(edata)):
            #  Tdata
            for k in range(len(hdata)):
                if edata[i][0] == hdata[k][1] and edata[i][1] == hdata[k][2] and edata[i][2] == hdata[k][3]:
                    for l in range(4, 28):
                        for x in range(3, 27):
                            ti, tj = time_milaune("hdata", i, x)
                            result2.append([edata[i][0], edata[i][1], edata[i][2], bsbaarfinder(edata[i][0], edata[i][1], edata[i][2]), x - 2, edata[i][x], hdata[hindex + ti][tj]])
                            print(edata[i][0], edata[i][1], edata[i][2],bsbaarfinder(edata[i][0], edata[i][1], edata[i][2]), x - 2, edata[i][x],hdata[hindex + ti][tj])
                        break
    except:
        print(result2)

    try:
        for i in range(len(result1)):
            for j in range(len(result2)):
                if result1[i][0] == result2[j][0] and result1[i][1] == result2[j][1] and result1[i][2] == result2[j][2] and result1[i][4] == result2[j][4]:
                    result.append([result1[i][0],result1[i][1],result1[i][2],result1[i][3],result1[i][4],result1[i][5], result1[i][6],result2[j][6]])
                    print(result1[i][0],result1[i][1],result1[i][2],result1[i][3],result1[i][4],result1[i][5],result1[i][6],result2[j][6])
                    #break
        return result, False
    except:
        return result, True

def generate_dataset(request):
    dataset = []
    con1 = mysql.connector.connect(host="localhost", user="root", passwd="", database="neadata")
    cursor1 = con1.cursor()
    sqlcommand1 = "TRUNCATE TABLE forecast_puredataset;"  # only kept to debug interpolation process works fine once interpolation is done
    cursor1.execute(sqlcommand1)
    #   Temperature data lera sablai euta array ma rakhne
    tdata = db_reader('adminpanel_tdataall',28,1)[0]
    #print(tdata,"\n")

    #   Humidity data lera sablai euta array ma rakhne
    hdata = db_reader("adminpanel_hdata",28,1)[0]
    #print(hdata,"\n")

    #   Electric data harek table ko lai eutai array ma rakhne
    rough = []
    edata = []
    rougheutaorw = []
    year = hdata[0][1]
    month = hdata[0][2]
    termination = 0
    while termination<6:
        dbname = "y" + str(year*100+month)
        if not db_table_exists(dbname):
            termination +=1
            #print(dbname, "payena")
        else:
            rough = []
            termination = 0
            #print(dbname, "payo")
            rough.extend(db_reader_hourly(dbname,1)[0])
            for i in range(len(rough)):
                rougheutaorw = [year,month,i+1] + rough[i]
                edata.append(rougheutaorw)
        month += 1
        if month > 12:
            year += 1
            month = 1
    #   Universal Dataset banaaune
    #   edata, hdata, tdata bata
    # print(edata)

    dataset,error = set_value(edata,tdata,hdata)
    print(dataset)
    err = 0
    print("try ko for ma xire")
    for i in range(len(dataset)):
        row = dataset[i]
        #print(i,"save gaarne")
        dset = puredataset();
        dset.year   = dataset[i][0]
        dset.month  = dataset[i][1]
        dset.day    = dataset[i][2]
        dset.baar   = dataset[i][3]
        dset.time   = dataset[i][4]
        dset.eldata = dataset[i][5]
        dset.tmdata = dataset[i][6]
        dset.hddata = dataset[i][7]
        dset.save()
        print(len(dataset),i)
        print("yo her")
        print(dset.day)
    print("try maa sakkiyo")
    return render(request, "fulldataset.html", {'dataset_creation': True,'error':error})

def pageholder(request):
    return render(request, "fulldataset.html")

def linearall(request):
    tuple_data = db_reader("forecast_puredataset", 9, 1)
    dato = pd.DataFrame(tuple_data[0],
                        columns=['id', 'year', 'month', 'day', 'baar', 'time', 'eldata', 'tmdata', 'hddata'])
    data = cleaner(dato)
    print(data.head)

    data = data[["month","day","baar","time","eldata"]]

    predict = "eldata"

    x = np.array(data.drop([predict],1))
    y = np.array(data[predict])
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    best = 0
    
    for _ in range(100):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.1)

        linear = linear_model.LinearRegression()
        linear.fit(x_train,y_train)
        acc = linear.score(x_test,y_test)
        tacc = linear.score(x_train,y_train)
        print(f"accuracy: {acc} tacc:{tacc}")

        if acc>best:
            best = acc
            with open("puredataset.pickle","wb") as f:
                pickle.dump(linear,f)

    print(f"best:{best}")
    """
    pickle_in = open("puredataset.pickle","rb")
    linear = pickle.load(pickle_in)
    #print("co: \n", linear.coef_)
    #print("Intercept: \n", linear.intercept_)
    """
    print(x_test)
    #x_test.shape(6,)
    linear.fit(x_train,y_train)
    predictions = linear.predict(x_test)


    perfect = 0
    match = 0
    unmatch = 0
    total = 0

    for x in range(len(predictions)):
        print(round(predictions[x],1), np.round(x_test[x],1), round(y_test[x],1))
        if round(float(predictions[x]),1)==float(round(y_test[x],1)): perfect += 1; print("perfect")
        elif abs(float(predictions[x])-float(y_test[x]))<=0.11: match += 1 ; print("matched",y_test[x],predictions[x])
        else: unmatch += 1 ; print("unmatched")
        total += 1
    
    sacc = (match+perfect)/total
    predictx = np.round(predictions,1)
    predictx = predictx.tolist()
    actualx = np.round(y_test,1)
    actualx = actualx.tolist()
    test = x_test.tolist()
    acc = linear.score(x_test,y_test)
    print(acc)
    print(predictx)
    print("Perfect: ",perfect," Matched :",match," Unmatched: ",unmatch," Total: ", total)
    print("Slight Accuracy: ",(match+perfect)*100/total)
    print("Raw Accuracy: ",acc)
    return render(request, "fulldataset.html", {'trained': True,'predicted': predictx, 'actual': actualx,"accuracy":acc,"saccuracy":sacc,"howmany":len(predictions),"xtest":test})


def knngenerate(request):
    bestacc = 0
    bestaccnb = 5

    nb = 20     #neighbours
    
    tuple_data = db_reader("forecast_puredataset", 9, 1)
    data = pd.DataFrame(tuple_data[0],
                        columns=['id', 'year', 'month', 'day', 'baar', 'time', 'eldata', 'tmdata', 'hddata'])
    
    #print(type(data))
    #print(data.head())
    #print(data.tail())
    le = preprocessing.LabelEncoder()
    #year = le.fit_transform(list(data["year"]))
    month = le.fit_transform(list(data["month"]))
    mlabel  = le.inverse_transform(month)

    day = le.fit_transform(list(data["day"]))
    dlabel  = le.inverse_transform(day)

    baar = le.fit_transform(list(data["baar"]))
    blabel  = le.inverse_transform(baar)

    time = le.fit_transform(list(data["time"]))
    tlabel  = le.inverse_transform(time)

    tmdata = le.fit_transform(list(data["tmdata"]))
    tmlabel = le.inverse_transform(tmdata)

    eldata = le.fit_transform(list(data["eldata"]))
    ellabel = le.inverse_transform(eldata)

    hddata = le.fit_transform(list(data["hddata"]))
    hdlabel = le.inverse_transform(hddata)

    edexact = list(data["eldata"])

    predict = "eldata"

    x = list(zip(month,day,baar,time,eldata))
    #z = list(zip(month,day,baar,time,eldata,tmdata,hddata))
    #x.extend(z)
    #print(x[14327])
    #print(x[14328])
    #print(x[28653])
    #print(x)

    y = list(eldata)

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.1)
    rmse_val = [] #to store rmse values for different k
    forgraph = [[0],[0]]

    for i in range(20):
        model = KNeighborsClassifier(n_neighbors=nb, weights='distance', algorithm='auto', leaf_size=40, p=1,metric='minkowski')

        model.fit(x_train,y_train)
        acc = model.score(x_test,y_test)
        #print(acc)


        predicted = model.predict(x_test)
       
        #error = sqrt(mean_squared_error(y_test,predicted)) #calculate rmse
        #rmse_val.append(error) #store rmse values
        #print('RMSE value for k= ' , nb , 'is:', error)
        
        perfect = 0
        match = 0
        unmatch = 0
        total = 0
        


        #print(x_test)
        for x in range(len(predicted)):
            mtest = month.tolist().index(x_test[x][0])
            dtest = day.tolist().index(x_test[x][1])
            btest = baar.tolist().index(x_test[x][2])
            ttest = time.tolist().index(x_test[x][3])
            eltest = eldata.tolist().index(x_test[x][4])
            #tmtest = tmdata.tolist().index(x_test[x][5])
            #hdtest = hddata.tolist().index(x_test[x][6])
            
            predtest = eldata.tolist().index(predicted[x])
            actutest = eldata.tolist().index(y_test[x])
            
            #print("Predicted: ", ellabel[predtest],"Data: ",mlabel[mtest],dlabel[dtest],blabel[btest],tlabel[ttest],tmlabel[tmtest],hdlabel[hdtest] ," Actual: ",ellabel[actutest])
            n = model.kneighbors([x_test[x]],nb,True)
            
            
            if float(ellabel[predtest])==float(ellabel[actutest]): perfect += 1; #print("perfect")
            elif abs(float(ellabel[predtest])-float(ellabel[actutest]))<=0.1: match += 1 ;# print("matched",edexact[y_test[x]],edexact[predicted[x]])
            else: unmatch += 1 ;# print("unmatched")
            total += 1

            # print("N: ",n)
        #print(data["baar"][x_test[x][2]])
        #print("Perfect: ",perfect," Matched :",match," Unmatched: ",unmatch," Total: ", total)
        tacc = (match/total)*100
        sacc = (match+perfect)*100/total
        #print("Slight Accuracy: ",(match+perfect)*100/total)
        #print("Raw Accuracy: ",acc)
        if acc>bestacc:
            bestacc = acc
            bestaccnb = nb
            print("<-------------------------neW best------------------>")
        print("Nb: ",nb,"Acc: ",round(acc,2),"SAcc: ",round(sacc,2),"perfect: ",perfect,"match: ",match,"unmatch: ",unmatch," ",total)
        nb += 1
    #if ((match+perfect)*100/total)>60:
        forgraph[0].append(nb)
        forgraph[1].append(acc)
    print(forgraph)
    
    facc = 0;

    x = list(zip(month,day,baar,time,eldata))
    y = list(eldata)
    for i in range(50):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.1)
        model = KNeighborsClassifier(n_neighbors=bestaccnb, weights='distance', algorithm='auto', leaf_size=40, p=1,
                                     metric='minkowski')
        model.fit(x_train,y_train) 
        acc = model.score(x_test,y_test)
        print("acc:",acc)
        if acc>facc:
            facc = acc
            with open("knnko.pickle", "wb") as f:
                nb = bestaccnb
                pickle.dump(model, f)
                print("<------------saved--------------->")

    return render(request, "fulldataset.html", {'trained': True})
    

def knnpredict(request):

    nb = 31  # neighbours
    tuple_data = db_reader("forecast_puredataset", 9, 1)
    dato = pd.DataFrame(tuple_data[0],
                        columns=['id', 'year', 'month', 'day', 'baar', 'time', 'eldata', 'tmdata', 'hddata'])
    
    data = cleaner(dato)
    print(type(data))
    print(data.head())
    # print(data.tail())
    le = preprocessing.LabelEncoder()
    # year = le.fit_transform(list(data["year"]))
    month = le.fit_transform(list(data["month"]))
    mlabel  = le.inverse_transform(month)

    day = le.fit_transform(list(data["day"]))
    dlabel  = le.inverse_transform(day)

    baar = le.fit_transform(list(data["baar"]))
    blabel  = le.inverse_transform(baar)

    time = le.fit_transform(list(data["time"]))
    tlabel  = le.inverse_transform(time)

    tmdata = le.fit_transform(list(data["tmdata"]))
    tmlabel = le.inverse_transform(tmdata)

    eldata = le.fit_transform(list(data["eldata"]))
    ellabel = le.inverse_transform(eldata)

    hddata = le.fit_transform(list(data["hddata"]))
    hdlabel = le.inverse_transform(hddata)

    edexact = list(data["eldata"])

    print(edexact)
    # yr = data["year"]
    mn = data["month"]
    dy = data["day"]
    br = data["baar"]
    tm = data["time"]

    print(month)
    print(le.inverse_transform(month))
    predict = "eldata"

    x = list(zip(month, day, baar, time, eldata))
    y = list(eldata)

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
    
    pickle_in = open("knnko.pickle","rb")
    model = pickle.load(pickle_in)
    #model = KNeighborsClassifier(n_neighbors=nb)

    model.fit(x_train, y_train)
    acc = model.score(x_test, y_test)

    predicted = model.predict(x_test)
    # names = ["unacc","acc","good","vgood"]
    perfect = 0
    match = 0
    unmatch = 0
    total = 0

    #for transport to frontend
    predictx = []
    test = []
    onerow = []
    actualx = []
    
    for x in range(len(predicted)):
        mtest = month.tolist().index(x_test[x][0])
        dtest = day.tolist().index(x_test[x][1])
        btest = baar.tolist().index(x_test[x][2])
        ttest = time.tolist().index(x_test[x][3])
        eltest = eldata.tolist().index(x_test[x][4])
        #tmtest = tmdata.tolist().index(x_test[x][5])
        #hdtest = hddata.tolist().index(x_test[x][6])
        
        predtest = eldata.tolist().index(predicted[x])
        actutest = eldata.tolist().index(y_test[x])
        
        
        
        #transport to frontend
        onerow.append(mlabel[mtest])
        onerow.append(dlabel[dtest])
        onerow.append(blabel[btest])
        onerow.append(tlabel[ttest])
        #onerow.append(tmlabel[tmtest])
        #onerow.append(hdlabel[hdtest])
        test.append(onerow)
        onerow = []
        predictx.append(ellabel[predtest])
        actualx.append(ellabel[actutest])
    
    
        #print("Predicted: ", ellabel[predtest],"Data: ",mlabel[mtest],dlabel[dtest],blabel[btest],tlabel[ttest],tmlabel[tmtest],hdlabel[hdtest] ," Actual: ",ellabel[actutest])
        n = model.kneighbors([x_test[x]], nb, True)
        if float(ellabel[predtest])==float(ellabel[actutest]): perfect += 1; print("perfect")
        elif abs(float(ellabel[predtest])-float(ellabel[actutest]))<=0.1: match += 1 ; print("matched",edexact[y_test[x]],edexact[predicted[x]])
        else: unmatch += 1 ; print("unmatched")
        total += 1
        # print("N: ",n)
    print(data["baar"][x_test[x][2]])
    print("Perfect: ", perfect, " Matched :", match, " Unmatched: ", unmatch, " Total: ", total)
    sacc = (match + perfect) * 100 / total
    print("Slight Accuracy: ", sacc)
    print("Raw Accuracy: ", acc)

    if ((match + perfect) * 100 / total) > 60:
        with open("puredataset.pickle", "wb") as f:
            pickle.dump(model, f)
            print("saved")

    return render(request, "fulldataset.html", {'predicted': predictx, 'actual': actualx,"accuracy":acc,"saccuracy":sacc,"howmany":len(predicted),"xtest":test})

def forecaster(request):
    nb = 31  # neighbours
    fortrain = pd.read_csv("out.csv")
    dato = pd.read_csv("demo.csv")
    pickle_in = open("knnko.pickle", "rb")
    model = pickle.load(pickle_in)
    # model = KNeighborsClassifier(n_neighbors=nb)
    # print(data.tail())
    le = preprocessing.LabelEncoder()
    for i in range(2):
        if i==0: data = fortrain;
        if i==1: data = dato;
        # year = le.fit_transform(list(data["year"]))
        month = le.fit_transform(list(data["month"]))
        mlabel = le.inverse_transform(month)

        day = le.fit_transform(list(data["day"]))
        dlabel = le.inverse_transform(day)

        baar = le.fit_transform(list(data["baar"]))
        blabel = le.inverse_transform(baar)

        time = le.fit_transform(list(data["time"]))
        tlabel = le.inverse_transform(time)

        tmdata = le.fit_transform(list(data["tmdata"]))
        tmlabel = le.inverse_transform(tmdata)

        eldata = le.fit_transform(list(data["eldata"]))
        ellabel = le.inverse_transform(eldata)

        hddata = le.fit_transform(list(data["hddata"]))
        hdlabel = le.inverse_transform(hddata)

        edexact = list(data["eldata"])

        #print(edexact)
        # yr = data["year"]
        mn = data["month"]
        dy = data["day"]
        br = data["baar"]
        tm = data["time"]

        if i==0:
            x = list(zip(month, day, baar, time, eldata))
            y = list(eldata)
            x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
            model.fit(x_train, y_train)

        if i==1:
            x = list(zip(month, day, baar, time, eldata))
            y = list(eldata)
            x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=.95,shuffle=False)
            acc = model.score(x_test, y_test)
            predicted = model.predict(x_test)

    #print(month)
    #print(le.inverse_transform(month))
    predict = "eldata"


    # names = ["unacc","acc","good","vgood"]
    perfect = 0
    match = 0
    unmatch = 0
    total = 0

    # for transport to frontend
    predictx = []
    test = []
    onerow = []
    actualx = []

    for x in range(len(predicted)):
        mtest = month.tolist().index(x_test[x][0])
        dtest = day.tolist().index(x_test[x][1])
        btest = baar.tolist().index(x_test[x][2])
        ttest = time.tolist().index(x_test[x][3])
        eltest = eldata.tolist().index(x_test[x][4])
        # tmtest = tmdata.tolist().index(x_test[x][5])
        # hdtest = hddata.tolist().index(x_test[x][6])

        predtest = eldata.tolist().index(predicted[x])
        actutest = eldata.tolist().index(y_test[x])

        # transport to frontend
        onerow.append(mlabel[mtest])
        onerow.append(dlabel[dtest])
        onerow.append(blabel[btest])
        onerow.append(tlabel[ttest])
        # onerow.append(tmlabel[tmtest])
        # onerow.append(hdlabel[hdtest])
        test.append(onerow)
        onerow = []
        predictx.append(ellabel[predtest])
        actualx.append(ellabel[actutest])

        print("Predicted: ", ellabel[predtest],"Data: ",mlabel[mtest],dlabel[dtest],blabel[btest],tlabel[ttest]," Actual: ",ellabel[actutest])
        n = model.kneighbors([x_test[x]], nb, True)
        if float(ellabel[predtest]) == float(ellabel[actutest]):
            perfect += 1; print("perfect")
        elif abs(float(ellabel[predtest]) - float(ellabel[actutest])) <= 0.12:
            match += 1; print("matched", edexact[y_test[x]], edexact[predicted[x]])
        else:
            unmatch += 1; print("unmatched")
        total += 1
        # print("N: ",n)
    #print(data["baar"][x_test[x][2]])
    print("Perfect: ", perfect, " Matched :", match, " Unmatched: ", unmatch, " Total: ", total)
    sacc = (match + perfect) * 100 / total
    print("Slight Accuracy: ", sacc)
    print("Raw Accuracy: ", acc)
    #predictx.tolist()
    print(type(predictx))
    print(type(test))
    print(test)
    naya = []
    for z in range(len(test)):
        naya.append([test[z],predictx[z],actualx[z]])
        #test[z].extend(predictx[z])
        #test[z].extend(actualx)
    naya = sortasc(naya)
    for z in range(len(predictx)):
        test[z] = naya[z][0]
        predictx[z] = naya[z][1]
        actualx[z] = naya[z][2]
    print(test)
    #print(predictx)
    #print(actualx)
    return render(request, "fulldataset.html", {'forecast':True,'predicted': predictx, 'actual': actualx,"accuracy":acc,"saccuracy":sacc,"howmany":len(predicted),"xtest":test})

def sortasc(list):
    min = 99
    for i in range(50):
        for i in range(len(list)-1):
            if list[i][0][3]>list[i+1][0][3]:
                list[i],list[i+1] = list[i+1],list[i]
    #print(list)
    return list

def cleaner(dato):

    data = dato[["month","day","baar","time","eldata","tmdata","hddata"]]
    predict = "eldata"
    elforor = []
    tmforor = []

    elstring = data["eldata"]
    for i in elstring:
        elforor.append(float(i))

    outlier = [1.1]
    #EL4ATA
    while len(outlier)>0:
        outlier = []
        maxvalue = 0
        minvalue = 10

        mean = np.mean(elforor)
        std = np.std(elforor)
        print('mean of the dataset is', round(mean,1))
        print('std. deviation is', round(std,1))
        q1 = np.percentile(elforor, 25,interpolation='midpoint')
        q2 = np.percentile(elforor, 50, interpolation='midpoint')
        q3 = np.percentile(elforor, 75, interpolation='midpoint')
        iqr = round(q3 - q1,1)
        lowerlimit = round(q1 - 0.4*iqr,1)
        upperlimit = round(1.5*iqr + q3,1)
        maxvalue = max(elforor)
        minvalue = min(elforor)
        print("Q1: ",q1,"Q2: ",q2,"Q3: ",q3)
        print("IQR ",iqr)
        print("lower : ",lowerlimit)
        print("upper : ",upperlimit)
        print("max: ",maxvalue)
        print("min: ",minvalue)

        for i in range(len(elforor)):
            if elforor[i]>upperlimit or elforor[i]<lowerlimit:
                outlier.append([i,elforor[i]])
        for i in range(len(outlier)):
            count = outlier[i][0]
            replace = (elforor[count-2]+elforor[count-1]+elforor[count+1]+elforor[count+2])/4
            print(count,")",elforor[count-2],elforor[count-1],elforor[count],elforor[count+1],elforor[count+2],"---->",round(replace,1))
            elforor[count] = round(replace,1)
        #quit = input("quit?")

    #TM4ATA
    tmforor = []
    elstring = data["tmdata"]
    for i in elstring:
        tmforor.append(float(i))

    outlier = [1.1]
    while len(outlier)>0:
        outlier = []
        maxvalue = 0
        minvalue = 10

        mean = np.mean(tmforor)
        std = np.std(tmforor)
        print('mean of the dataset is', round(mean,1))
        print('std. deviation is', round(std,1))
        q1 = np.percentile(tmforor, 25,interpolation='midpoint')
        q2 = np.percentile(tmforor, 50, interpolation='midpoint')
        q3 = np.percentile(tmforor, 75, interpolation='midpoint')
        iqr = round(q3 - q1,1)
        lowerlimit = round(q1 - 1.5*iqr,1)
        upperlimit = round(1.5*iqr + q3,1)
        maxvalue = max(tmforor)
        minvalue = min(tmforor)
        print("Q1: ",q1,"Q2: ",q2,"Q3: ",q3)
        print("IQR ",iqr)
        print("lower : ",lowerlimit)
        print("upper : ",upperlimit)
        print("max: ",maxvalue)
        print("min: ",minvalue)

        for i in range(len(tmforor)):
            if tmforor[i]>upperlimit or tmforor[i]<lowerlimit:
                outlier.append([i,tmforor[i]])
        for i in range(len(outlier)):
            count = outlier[i][0]
            replace = (tmforor[count-2]+tmforor[count-1]+tmforor[count+1]+tmforor[count+2])/4
            print(count,")",tmforor[count-2],tmforor[count-1],tmforor[count],tmforor[count+1],tmforor[count+2],"---->",round(replace,1))
            tmforor[count] = round(replace,1)

    #H44ATA
    quit = ""
    hdforor = []
    elstring = data["hddata"]
    for i in elstring:
        hdforor.append(float(i))

    outlier = [1.1]
    berserker = 0
    while len(outlier)>0:
        berserker += 1
        outlier = []
        maxvalue = 0
        minvalue = 10

        mean = np.mean(hdforor)
        std = np.std(hdforor)
        print('mean of the dataset is', round(mean,1))
        print('std. deviation is', round(std,1))
        q1 = np.percentile(hdforor, 25,interpolation='midpoint')
        q2 = np.percentile(hdforor, 50, interpolation='midpoint')
        q3 = np.percentile(hdforor, 75, interpolation='midpoint')
        iqr = round(q3 - q1,1)
        lowerlimit = round(q1 - 1.5*iqr,1)
        upperlimit = round(100)
        maxvalue = max(hdforor)
        minvalue = min(hdforor)
        print("Q1: ",q1,"Q2: ",q2,"Q3: ",q3)
        print("IQR ",iqr)
        print("lower : ",lowerlimit)
        print("upper : ",upperlimit)
        print("max: ",maxvalue)
        print("min: ",minvalue)

        for i in range(len(hdforor)):
            if hdforor[i]>upperlimit or hdforor[i]<lowerlimit:
                outlier.append([i,hdforor[i]])
                
        for i in range(len(outlier)):
            count = outlier[i][0]
            if hdforor[count]>100: replace = 100
            elif (hdforor[count]<lowerlimit-5): replace =  hdforor[count] + 10
            elif (berserker>200): replace = hdforor[count-1]        # purge the heretic values
            else: replace = (hdforor[count-2]+hdforor[count-1]+hdforor[count+1]+hdforor[count+2])/4
            print(count,")",hdforor[count-2],hdforor[count-1],hdforor[count],hdforor[count+1],hdforor[count+2],"---->",round(replace,1))
            hdforor[count] = round(replace,1)

    df = pd.DataFrame({'month': data["month"],
                   'day': data["day"],
                   'baar': data["baar"],
                   'time': data["time"],
                   'eldata': elforor,
                   'tmdata': tmforor,
                   'hddata': hdforor
                   })
    return df