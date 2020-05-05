# BeyondPing

Ping a bunch of public DNS servers across the world and plot the response times in the form of a map

Dependenencies: -Python3.7 -Numpy -Matplotlib -basemap -pandas -pyproj -wheel -geocoder

Application uses multiprocessing to speed up the process. Pinging IP's over an iterative loop would take a hell lot of time. Suppose, I had 5000 IP addresses that I would want to ping. It would approximately take 500ms for each ping, which sums up to a total of 2500 seconds (ignoring the intermediary processing). Using PingTheWorld it only takes about 60-70 seconds to ping 5000 IP addresses, thanks to multiprocessing. But of course, this application requires a lot of memory to reduce the time taken. Would suggest to increase/decrease number of processes in the multiprocessing pool as per installed RAM and processing capacity. 

Source code and complete directory uploaded

![Sample](https://github.com/vsrivatsa25/BeyondPing/blob/master/example.png)
