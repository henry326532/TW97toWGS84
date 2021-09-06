import json
import math

#讀入檔案
file1 = open('TP_Ramp.geojson','r', encoding='utf-8')
word = file1.read()
json1 = json.loads(word)

#匯出檔案
def write_to_file(content):
    with open('result.json','a',encoding='CP950') as f:
        f.write(json.dumps(content,ensure_ascii=True))


#TWD97 transfer GWS84 的參數
pi = math.pi
a = 6378137.0
b = 6356752.314245
lon0 = 121 * pi / 180
k0 = 0.9999
dx = 250000
dy = 0
e = (1 - b**2 / a**2)**0.5


for feature in json1['features']:

    input_lat = feature['geometry']['coordinates'][0]
    input_lon = feature['geometry']['coordinates'][1]

    x =  input_lat - dx # input_lat: TWD97橫座標, 緯度, latitud
    y =  input_lon - dy # input_lon: TWD97縱座標, 經度, longitude

    M = y/k0

    mu = M/(a*(1.0 - ( e**2 )/4.0 - 3* (e**4)/64.0 - 5* (e**6)/256.0))
    e1 = (1.0 -  ((1.0 -  (e**2))**0.5)) / (1.0 +  ((1.0 -  (e**2))**0.5))

    J1 = (3*e1/2 - 27* (e1**3)/32.0)
    J2 = (21* (e1**2)/16 - 55* (e1**4)/32.0)
    J3 = (151* (e1**3)/96.0)
    J4 = (1097* (e1**4)/512.0)

    fp = mu + J1*math.sin(2*mu) + J2*math.sin(4*mu) + J3*math.sin(6*mu) + J4*math.sin(8*mu)

    e2 =  ((e*a/b)**2)
    C1 =  (e2*math.cos(fp)**2)
    T1 =  (math.tan(fp)**2)
    R1 = a*(1- (e**2))/ ((1- (e**2)* (math.sin(fp)**2))**(3.0/2.0))
    N1 = a/ ((1- (e**2)* (math.sin(fp)**2))**0.5)

    D = x/(N1*k0)

    #緯度計算 latitude
    Q1 = N1*math.tan(fp)/R1
    Q2 = ( (D**2)/2.0)
    Q3 = (5 + 3*T1 + 10*C1 - 4* (C1**2) - 9*e2)* (D**4)/24.0
    Q4 = (61 + 90*T1 + 298*C1 + 45* (T1**2) - 3* (C1**2) - 252*e2)* (D**6)/720.0
    lat = fp - Q1*(Q2 - Q3 + Q4)

    #經度計算 longitude
    Q5 = D
    Q6 = (1 + 2*T1 + C1)* (D**3)/6
    Q7 = (5 - 2*C1 + 28*T1 - 3* (C1**2) + 8*e2 + 24* (T1**2))* (D**5)/120.0
    lon = lon0 + (Q5 - Q6 + Q7)/math.cos(fp)

    lat = (lat*180) /pi #南北緯度  latitude 
    lon = (lon*180)/ pi #東西經度  longitude

    feature['geometry']['coordinates'][0] = lon
    feature['geometry']['coordinates'][1] = lat
    feature['properties']['X'] = [lat,lon]
    feature['properties']['Y'] = lon
    

write_to_file(json1)