import time
import multiprocessing
import subprocess
import re
import geocoder
import random
import pandas as pd

#open csv file containing dns servers data using pandas
df_csv = pd.read_csv('nameservers.csv', encoding='latin-1', engine='python')
lines = [list(x) for x in df_csv.values]

#function to pick color from gradient based on latency
def colorpicker(latency):
    if latency<=15:
        hexcode = hex(int(latency * 255 / 200))[-1:] + "fff" + "00"
    elif latency<=200 and latency>15:
        hexcode=hex(int(latency*255/200))[-2:]+"ff"+"00"
    elif latency>200 and latency <=600:
        hexcode="ff"+hex(int((600-latency)*255/400))[-2:]+"00"
    else:
        hexcode="ffff00"
    return (str("#"+hexcode))

#function to ping given IP address and return response time
def osping(ip):
    try:
        command = 'ping ' + ip + ' -n 1 -l 1 -w 1000'
        ans = str(subprocess.check_output(command, shell=True))
    except:
        return '-'
        pass
    else:
        pattern = "(time)=([0-9]+)ms TTL"
        regex = re.compile(pattern)
        ans2 = regex.findall(ans)
        if len(ans2)==1:
            return ans2[0][1]
        else:
            return '-'

#function to get coordinates of a city of DNS server
def getcoordinates(loc):
    try:
        g = geocoder.geonames(loc, key="KEY")
        #replace KEY with your geonames api key. Register at https://www.geonames.org/
        longitude = g.lng
        latitude = g.lat
        return (float(longitude),float(latitude))
    except:
        return 'NA','NA'

#multiprocessing function which calls the other functions required to ping and obtain coordinates
def multiprocessing_func(i):
    randip=lines[i][0]
    try:
        ans = osping(randip)
        lines[i][10] = ans
        if lines[i][11]=="-" and ans!='-':
            if i>0 and lines[i][3]==lines[i-1][3] and lines[i-1][11]!='-' and lines[i-1][11]!='NA':
                lines[i][11] = lines[i-1][11]
                lines[i][12] = lines[i-1][12]
            else:
                try:
                    coords=getcoordinates(lines[i][3]+", "+lines[i][2])
                    lines[i][11] = coords[0]
                    lines[i][12] = coords[1]
                except TypeError or IndexError:
                     pass
        return lines[i]
    except OSError or AttributeError or GeocoderTimedOut:
        lines[i][10] = '-'
        return lines[i]

if __name__ == '__main__':
    starttime = time.time()
    #set number of processes basd on your CPU capacity
    pool = multiprocessing.Pool(processes=33)
    print("Starting the ping process...")
    vals = pool.map(multiprocessing_func, range(5527))
    print("Ping successful...")
    print('That took {} seconds...'.format(time.time() - starttime))
    pool.close()

    from numpy import arange as arange
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from datetime import datetime

    #world map to plot cities and response times
    map = Basemap()
    fig = plt.figure(figsize=(12, 9))
    map.drawcoastlines()
    map.drawparallels(arange(-90, 90, 10), labels=[1, 0, 0, 0])
    map.drawmeridians(arange(map.lonmin, map.lonmax + 30, 20), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='white', lake_color='aqua')
    map.drawcountries()
    date = datetime.utcnow()
    plt.title('Ping Response Time Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))

    starttime = time.time()
    print("Updating data...")
    ciy = []
    #for loop to plot points and update csv file
    for i in range(len(vals)):
        if vals[i][10] != '-' and vals[i][3] not in ciy and vals[i][11]!='NA':
            ciy.append(vals[i][3])
            try:
                map.scatter(float(vals[i][11]), float(vals[i][12]), c=colorpicker(int(vals[i][10])), s=30, zorder=2,
                            alpha=1)
                plt.annotate(vals[i][3] + " " + vals[i][2] + "\n" + "Latency:" + vals[i][10] + "ms",
                             (float(vals[i][11]), float(vals[i][12])), size=6)
            except:
                pass
        df_csv._set_value(i, 'response_time', vals[i][10])
        df_csv._set_value(i, 'longitude', vals[i][11])
        df_csv._set_value(i, 'latitude', vals[i][12])

    self_loc = geocoder.ip('me')
    map.scatter(self_loc.lng, self_loc.lat, c='blue', s=90, zorder=3, alpha=1)
    plt.annotate("I am here!", (self_loc.lng, self_loc.lat), size=7)
    df_csv.to_csv('nameservers.csv', index=False)
    print('That took {} seconds...'.format(time.time() - starttime))
    print("IP Data inserted successfully into table...")
    print("Plotting Map...")
    plt.show()
    print("Map Closed...")

    # Created by : Vrishab V Srivatsa
    # Credits : Geocoder API, https://public-dns.info 
    # Inspired by a Cloudflare internship application task
    # Please credit if used for your personal/academic uses
    # Twitter: @vsrivatsa25 https://twitter.com/vsrivatsa25?lang=da
    # Instagram: @vsrivatsa25 https://www.instagram.com/vsrivatsa25/?hl=en
