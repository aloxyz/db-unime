import os
import matplotlib.pyplot as plt
import numpy as np
import csv

mongo = neo4j = []
f25 = f50 = f75 = f100 = None

for i in range(25, 101, 25):
    directory = 'data/results/mongo/' + str(i)
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        with open(f,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ',')
            
            mean = list(plots)[31]
            mongo.append(mean[1] * 1000)
    

for i in range(25, 101, 25):
    directory = 'data/results/neo/' + str(i)
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        with open(f,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ',')
            
            mean = list(plots)[31]
            neo4j.append(mean[1] * 1000)


labels = ['25%', '50%', '75%', '100%']
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, neo4j, width, label='Neo4j')
rects2 = ax.bar(x + width/2, mongo, width, label='MongoDB')
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Tempo (Millisecondi)')
ax.set_title('Dimensione del dataset')
ax.set_xticks(x, labels)
ax.legend()

fig.tight_layout()
plt.legend()

f25 = plt.figure(1)
f50 = plt.figure(2)
f75 = plt.figure(3)
f100 = plt.figure(4)

f25.show()
f50.show()
f75.show()
f100.show()