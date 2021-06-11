# actual cubic spline interpolation code
def cubic_spline(xvals,mylist):
    #print(f"mylisttype : {type(mylist)}")
    #print(f"mylistleng : {len(mylist)}")
    #print(xvals)
    #xvals = [1,2,3,4,5,6,6.5,7,7.5,8,9,10,11,12,13,14,15,16,17,17.5,18,18.5,19,19.5,20,21,22,23,24]
    print(mylist)
    n = 0
    int_val = 0
    times = xvals
    y = [0.0]*len(times)
    for i in range(len(mylist)):
        if mylist[i]!=int_val:           # what to replacec
            n+=1
    #print(f"n in mylist = {n}")
    #Step 0
    n -= 1
    x = [0.0]*(n+1)
    a = [0.0]*(n+1)
    h = [0.0]*(n)
    A = [0.0]*n
    l = [0.0]*(n+1)
    u = [0.0]*(n+1)
    z = [0.0]*(n+1)
    c = [0.0]*(n+1)
    b = [0.0]*(n)
    d = [0.0]*(n)
    miss = 0
    #print("x ra a ko value halyo")
    for i in range(len(xvals)):
        if mylist[i]!=int_val:       #what to replace
            x[i-miss] = times[i]
            a[i-miss] = mylist[i]
            #print(f"{x[i-miss]} : {a[i-miss]}")
        else:
            miss += 1
    #print(f"miss:{miss}")
    if miss==0:
        #print("miss rainaxa farkum")
        return mylist

    # Step 1
    for i in range(n):
        h[i] = x[i+1] - x[i]

    # Step 2
    for i in range(1,n):
        A[i] = 3 * (a[i + 1] - a[i]) / h[i] - 3*(a[i] - a[i - 1]) / h[i-1]
        pass

    # Step 3
    l[0] = 1
    u[0] = 0
    z[0] = 0

    # Step 4
    for i in range(1,n):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * u[i - 1]
        u[i] = h[i] / l[i]
        z[i] = (A[i] - h[i - 1] * z[i - 1]) / l[i]

    # Step 5
    l[n] = 1
    z[n] = 0
    c[n] = 0

    # Step 6
    for j in range(n-1,0-1,-1):
        c[j] = z[j] - u[j] * c[j + 1]
        b[j] = (a[j + 1] - a[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    # Step 7
    #print("i ai bi ci di")
    for i in range(0,n):
        pass
        #print(f"{i} {a[i]} {b[i]} {c[i]} {d[i]}")

    for i in range(0,n):
        pass
        #print(f"P{i}(x) [{x[i]},{x[i + 1]}] = {d[i]}*(x-{x[i]})^3+{c[i]}*(x-{x[i]})^2+{b[i]}*(x-{x[i]})+{a[i]}\n")

    #print("mukhya hisab ma pugyo")
    for t in range(len(times)):
        if mylist[t]==int_val:
            for i in range(n):
                if times[t]>x[i] and times[t]<=x[i+1]:
                    y[t] = d[i]*(times[t]-x[i])**3 + c[i]*(times[t]-x[i])**2 + b[i]*(times[t]-x[i]) + a[i]
                    y[t] = round(y[t],1)
                    #print(f"P({times[t]}) [{x[i]},{x[i + 1]}] = {d[i]}*({times[t]}-{x[i]})^3+{c[i]}*({times[t]}-{x[i]})^2+{b[i]}*({times[t]}-{x[i]})+{a[i]} = {y[t]}\n")
                    continue
        else:
            y[t] = mylist[t]
        #print(f"{times[t]} : {y[t]}")
    print("spline complete vayo")
    print(y)
    return y

# consecutive data po missing xaki xaina vaera herne
def interpollable(mylist):
    for i in range(len(mylist)-1):
        if (mylist[i]==0.0 and mylist[i+1]==0.0):
            return False
    return True

# averager ko kaam:
# consecutive thuprai data missing rahexa vane mathiko row ra talako row bata average line
# missing ko first point ra +1 second ko point ma largest kunxa tesko ko corrensponding mathi or talako average linxa
# average liyesi ek xodera arko data check garxa
def averager(mylist0,mylist,mylist2):
    #print("averager mai adko")
    if mylist2 == None:
        mylist2 = mylist0
        #print("lstko list ma aipugera xaina vanne tahpaye")
    if mylist0 == None:
        mylist0 = mylist2

    i = 0

    while i < len(mylist)-1:
        if mylist[i]==0 and mylist[i+1]==0 and mylist2[i]!=0 and mylist0[i]!=0:
            if (mylist0[i]>=mylist0[i+1] and mylist2[i]>=mylist2[i+1]):
                mylist[i] = round((mylist2[i]+mylist0[i])/2,1)
                i += 1
            else:
                mylist[i+1] = round((mylist2[i+1]+mylist0[i+1])/2,1)
                i += 1
        if mylist[i]==0 and mylist[i+1]==0 and mylist2[i]==0 and mylist0[i]!=0:
            mylist[i] = round(mylist0[i],1)
        if mylist[i]==0 and mylist[i+1]==0 and mylist0[i]==0 and mylist2[i]!=0:
            mylist[i] = round(mylist2[i],1)
        i+=1

    # LASTKO laia 0 nai rakhyo teskolagi
    if mylist[i]==0:
        if mylist0[i]!=0 and mylist2[i]!=0: mylist[i]=(mylist0[i]+mylist2[i])/2
        if mylist0[i] == 0 and mylist2[i] != 0: mylist[i] = mylist2[i]
        if mylist0[i] != 0 and mylist2[i] == 0: mylist[i] = mylist0[i]
    #print("averager bata niskiyo")
    return mylist

#print(interpollable([0,1,1,1,1,0,1,1,1,0]))
#print(cubic_spline([0.6,0.6,0.6,0.6,0.7,1,1,1.2,1.3,1.3,1.3,1.3,1.2,1,1,0.9,1,1,1,1,1.2,1.3,1.6,1.6,1.5,1.3,1.1,0.8,0.7]))
#d = [0.0]*8
#d[1] = [1,2,3,4,5,4,3,2]
#d[2] = [1,2,0,0,5,0,0,1]
#d[3] = [1,2,4,5,5,4,3,2]
#averager(d[1],d[2],d[3])
#print(d[2])


#print(cubic_spline([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],[94.2,0,0,0,0,0,0,0,0,82.4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96.6]))
