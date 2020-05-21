import numpy as np
import matplotlib.pyplot as plt

#plt.suptitle('CDF of TCP Traceroutes')
'''
stats = ["FV Document Complete Median","FV Fully Loaded Median", "FV First Byte Median", "FV Start Render Median", "FV Requests (Doc) Median","FV Load Event Start Median", "FV Speed Index Median", "FV Last Visual Change Median", "FV Visually Complete Median"]
stats = [i[3:] for i in stats]
cores_1 = [67.0, 53.77, -2.06, -40.75, 69.77, 68.39, 27.98, 64.76, 58.07] 
cores_2 = [48.52, 37.97, 4.32, -61.11, 74.0, 55.65, 20.87, 49.48, 53.12]
cores_3 = [59.52, 52.63, 7.08, -29.23, 69.14, 65.7, 16.19, 53.52, 52.95]
simple_cores_4 =  [63.46, 46.32, 3.38, -50.3, 83.52, 62.81, 33.13, 66.09, 64.07]
'''

# Start Render, Requests, First Byte, Speed Index removed
stats = ["FV Document Complete Median","FV Fully Loaded Median", "FV Load Event Start Median", "FV Last Visual Change Median", "FV Visually Complete Median"]
stats = [i[3:] for i in stats]
cores_1 = [67.0, 53.77, 68.39, 64.76, 58.07] 
cores_2 = [48.52, 37.97, 55.65, 49.48, 53.12]
cores_3 = [59.52, 52.63, 65.7, 53.52, 52.95]
simple_cores_4 =  [63.46, 46.32, 62.81, 66.09, 64.07]


improv_dict = dict()
for i,stat in enumerate(stats):
    improv_dict[stat] = [ cores_1[i], cores_2[i], cores_3[i], simple_cores_4[i] ]

x = [1,2,3,4]
#x.reverse()
width = 0
for k,v in improv_dict.items():
    print(k,v)
    #v.reverse()
    print(x,v)
    x_axis = [i+width for i in x]
    width += 0.07

    plt.bar(x_axis, height=v, width=0.05)
    
    #plt.plot(x, v)


#plt.xlim(4, 1)
x_ticks = range(1, len(x)+1)
y_ticks = range(0, 101, 10)

plt.xticks(x_ticks)
plt.yticks(y_ticks)
#plt.ylim(-70,90)
#plt.plot(x, y)
plt.legend(stats, loc= "top right")

#plt.title("Hop Away From Server")
plt.xlabel("CPU Cores")
plt.ylabel("% Improvement for AMP")

plt.show()
plt.savefig("improv.png")