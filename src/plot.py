import os
import matplotlib.pyplot as plt
import numpy as np
import csv

mongo = []
neo = []
queryn = 1

for i in range(25, 101, 25):
    directory_mongo = 'data/results/mongo/' + str(i)
    directory_neo = 'data/results/neo/' + str(i)
    
    name = '/query_' + str(queryn) + '_load_' + str(i) + '.csv'
    f_mongo = directory_mongo + name
    f_neo = directory_neo + name

    with open(f_mongo,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter = ',')
        
        mean = list(plots)[31]
        mongo.append(mean[1])

    with open(f_neo,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter = ',')
        
        mean = list(plots)[31]
        neo.append(mean[1])




labels = ['25%', '50%', '75%', '100%']
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, neo, width, label='Neo4j')
rects2 = ax.bar(x + width/2, mongo, width, label='MongoDB')
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Tempo (Millisecondi)')
ax.set_title('2 WHERE')
ax.set_xticks(x, labels)
ax.legend()

fig.tight_layout()
plt.legend()
plt.show()
