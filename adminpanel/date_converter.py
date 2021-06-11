
def bs_months(year):
    all = []
    bs = [[0]*14]*100
    try:
        bs[0] = [2000, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[1] = [2001, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[2] = [2002, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[3] = [2003, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[4] = [2004, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[5] = [2005, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[6] = [2006, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[7] = [2007, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[8] = [2008, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31]
        bs[9] = [2009, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]

        bs[10] = [2010, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[11] = [2011, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[12] = [2012, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30]
        bs[13] = [2013, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[14] = [2014, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[15] = [2015, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[16] = [2016, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30]
        bs[17] = [2017, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[18] = [2018, 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[19] = [2019, 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]

        bs[20] = [2020, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[21] = [2021, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[22] = [2022, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30]
        bs[23] = [2023, 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[24] = [2024, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[25] = [2025, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[26] = [2026, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[27] = [2027, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[28] = [2028, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[29] = [2029, 31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30]

        bs[30] = [2030, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[31] = [2031, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[32] = [2032, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[33] = [2033, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[34] = [2034, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[35] = [2035, 30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31]
        bs[36] = [2036, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[37] = [2037, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[38] = [2038, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[39] = [2039, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30]

        bs[40] = [2040, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[41] = [2041, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[42] = [2042, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[43] = [2043, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30]
        bs[44] = [2044, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[45] = [2045, 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[46] = [2046, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[47] = [2047, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[48] = [2048, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[49] = [2049, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30]

        bs[50] = [2050, 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[51] = [2051, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[52] = [2052, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[53] = [2053, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30]
        bs[54] = [2054, 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[55] = [2055, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[56] = [2056, 31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30]
        bs[57] = [2057, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[58] = [2058, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[59] = [2059, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]

        bs[60] = [2060, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[61] = [2061, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[62] = [2062, 30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31]
        bs[63] = [2063, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[64] = [2064, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[65] = [2065, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[66] = [2066, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31]
        bs[67] = [2067, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[68] = [2068, 31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[69] = [2069, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]

        bs[70] = [2070, 31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30]
        bs[71] = [2071, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[72] = [2072, 31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30]
        bs[73] = [2073, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
        bs[74] = [2074, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[75] = [2075, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[76] = [2076, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30]
        bs[77] = [2077, 31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]
        bs[78] = [2078, 31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30]
        bs[79] = [2079, 31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30]

        bs[80] = [2080, 31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30]
        bs[81] = [2081, 31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[82] = [2082, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[83] = [2083, 31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[84] = [2084, 31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[85] = [2085, 31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30]
        bs[86] = [2086, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[87] = [2087, 31, 31, 32, 31, 31, 31, 30, 30, 29, 30, 30, 30]
        bs[88] = [2088, 30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30]
        bs[89] = [2089, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30]
        bs[90] = [2090, 30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30]

        all = bs[year%100]
        return (all)
    except:
        return None

def ad_months(year):
    normal_year = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    leap_year   = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    if year%4==0: return leap_year
    else: return normal_year

def adtobs(year,month,day):

    baar = ["saturday","sunday","monday","tuesday","wednesday","thursday","friday"]
    saal = 0
    mahina = 1
    gatey = 2
    #gate = [2000,1,1,4]
    #tarik = [1943,4,14,4]
    gate = [2073,1,1,4]
    tarik = [2016,4,13,4]
    total_days = 0
    adtotal_days = 0
    if ((year+month/12+day/365)>(gate[0]+gate[1]/12+gate[2]/365)):
        step = 1
    else: step = -1

    while tarik[saal]!=year or tarik[mahina]!=month or tarik[gatey]!=day:
        tarik[gatey] += 1
        tarik[3] += 1

        #print(tarik[mahina])
        total_days = ad_months(tarik[saal])[tarik[mahina]]
        if tarik[gatey]>total_days:
            tarik[mahina] +=1
            tarik[gatey] = 1

        if tarik[mahina]>12:
            tarik[saal] += 1
            tarik[mahina] = 1

        #if tarik[gatey]==total_days:
         #   print(f"{tarik[0]} {tarik[1]} {tarik[2]} : {total_days}")

        adtotal_days += 1

    #adtotal_days +=1    #+1 garnaa parne raixa
    #print(f"total days: {adtotal_days}")
    gate[2] += adtotal_days
    while gate[2]>bs_months(gate[0])[gate[1]]:
        gate[2] -= bs_months(gate[0])[gate[1]]
        gate[3] += bs_months(gate[0])[gate[1]]
        gate[1] += 1
        if gate[1]>12:
            gate[1] = 1
            gate[0] += 1
       # print(f"{gate[0]} {gate[1]} {gate[2]}")
    gate[3] = tarik[3]%7
    print("B.S. return garyoo")
    return (gate)

def bsbaarfinder(year,month,day):
    # gate = [2000,1,1,4]
    # tarik = [1943,4,14,4]
    gate = [2073, 1, 1, 4]
    mero = [year,month,day]

    while gate[0]!=mero[0] or gate[1]!=mero[1] or gate[2]!=mero[2]:
        gate[2]+=1
        gate[3]+=1
        gate[3] = gate[3] % 7
        if gate[2]>bs_months(gate[0])[gate[1]]:
            gate[1] += 1
            gate[2] = 1
        if gate[1]>12:
            gate[1] = 1
            gate[0] += 1

        #print("year",gate[0]," month ",gate[1]," day ",gate[2])
    return gate[3]

#print(bs_months(2077))
#print(ad_months(2000))
#print(adtobs(1998,8,10))
#print(f"{adtobs(2020,9,19)}")
#print(adtobs(1974,6,20))
#print(adtobs(1967,12,10))
#print(bsbaarfinder(2077,6,30))
#print(bsbaarfinder(2073,1,3))