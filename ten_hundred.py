def load_data(filepath):
    import csv
    file=open(filepath)
    file_reader=csv.reader(file)
    data=list(file_reader)
    return data[1:]
def calculate_x_y(time_series):
    n=int(time_series[-1])
    y=0
    x=0
    for i in range(4,len(time_series)):
        temp=int(time_series[i])
        if temp<=n/10:
            x=len(time_series)-i-1
        if temp<=n/100:
            y=len(time_series)-i-1
    return(x,y-x)
def hac(dataset):
    import copy
    cluster=[]
    for i in range(len(dataset)):
        subclus=[]
        yui=calculate_x_y(dataset[i])
        if yui[1]<0:
            continue
        if yui[0]==0 and yui[1]==0:
            continue
        subclus.append(yui)
        cluster.append(subclus)
    matrix = []
    numcluster=len(cluster)
    while numcluster>1:
        minim=99
        theclus=None
        theclus2=None
        for clus in range(len(cluster)-1):
            for clus2 in range(clus+1,len(cluster)):
                if cluster[clus]!=0 and cluster[clus2]!=0:
                    minim2=99
                    for u in cluster[clus]:
                        for v in cluster[clus2]:
                            temp=dist(u,v)
                            if temp<minim2:
                                minim2=temp
                    if minim2<minim:
                        minim=minim2
                        theclus=clus
                        theclus2=clus2
        if minim==99:
            break
        row=[0]*4
        row[3]=len(cluster[theclus2])+len(cluster[theclus])
        row[0]=theclus
        row[1]=theclus2
        for elem in cluster[theclus2]:
            cluster[theclus].append(elem)
        thetemp=copy.deepcopy(cluster[theclus])
        cluster.append(thetemp)
        cluster[theclus]=0
        cluster[theclus2]=0
        row[2]=minim
        matrix.append(row)
        for elem in cluster:
            if elem!=0:
                numcluster=numcluster+1
    import numpy as np
    return np.array(matrix)
def dist(x,y):
    import math
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance
dataset=load_data('time_series_covid19_confirmed_global.csv')
print(len(dataset))
print(hac(dataset))
