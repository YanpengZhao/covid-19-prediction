def get_dataset():
    from bs4 import BeautifulSoup
    import requests as req
    resp = req.get("http://www.aos.wisc.edu/~sco/lakes/Mendota-ice.html")
    soup = BeautifulSoup(resp.text, 'lxml')
    toreturn=str(soup.contents[0]).split('<br/>')
    toreturn.pop(0)
    toreturn.pop(-1)
    toreturn.pop(-1)
    year=[]
    days=[]
    mul=[]
    for y in range(1855,2020):
        year.append(y)
    for i in range(len(toreturn)):
        temp=toreturn[i]
        if "\n" in temp:
            toreturn[i]=toreturn[i].replace("\n",'')
        yui=toreturn[i].split(">")
        yuo=toreturn[i].split("<")
        if yui[-1].strip().isdecimal():
            days.append(int(yui[-1]))
        elif yuo[0].strip().isdecimal():
            days.append(int(yuo[0]))
    for p in range(len(year)):
        temp=[year[p],days[p]]
        mul.append(temp)
    return mul

def print_stats(dataset):
    print(len(dataset))
    total=0
    for arr in dataset:
        total=total+arr[1]
    mean=total/len(dataset)
    print(round(mean,2))
    import statistics
    tocal=[]
    for au in dataset:
        tocal.append(au[1])
    print(round(statistics.stdev(tocal),2))

def regression(beta_0,beta_1):
    data=get_dataset()
    sum=0
    for i in data:
        sum=sum+(beta_0+beta_1*i[0]-i[1])**2
    return sum/len(data)


def norm_regression(beta_0,beta_1):
    data = get_dataset()
    sum = 0
    for p in data:
        sum = sum + p[0]
    mean = sum / len(data)
    import statistics
    tocal = []
    for au in data:
        tocal.append(au[0])
    std = statistics.stdev(tocal)
    for o in range(len(data)):
        data[o][0] = (data[o][0] - mean) / std
    sum = 0
    for i in data:
        sum = sum + (beta_0 + beta_1 * i[0] - i[1]) ** 2
    return sum / len(data)


def gradient_descent(beta_0,beta_1):
    data = get_dataset()
    sum1 = 0
    sum2=0
    for i in data:
        sum1=sum1+(beta_0+beta_1*i[0]-i[1])
    for j in data:
        sum2=sum2+(beta_0+beta_1*j[0]-j[1])*j[0]
    return((sum1/len(data))*2,(sum2/len(data))*2)


def normal_grad(beta_0,beta_1):
    data = get_dataset()
    sum=0
    for p in data:
        sum=sum+p[0]
    mean=sum/len(data)
    import statistics
    tocal = []
    for au in data:
        tocal.append(au[0])
    std=statistics.stdev(tocal)
    for o in range(len(data)):
        data[o][0]=(data[o][0]-mean)/std
    sum1 = 0
    sum2 = 0
    for i in data:
        sum1 = sum1 + (beta_0 + beta_1 * i[0] - i[1])
    for j in data:
        sum2 = sum2 + (beta_0 + beta_1 * j[0] - j[1]) * j[0]
    return ((sum1 / len(data)) * 2, (sum2 / len(data)) * 2)


def iterate_gradient(T, eta):
    beta0=0
    beta1=0
    for i in range(1,T+1):
        beta0=beta0-eta*(gradient_descent(beta0,beta1)[0])
        beta1=beta1-eta*(gradient_descent(beta0,beta1)[1])
        print(str(i)+" "+str(round(beta0,2))+" "+str(round(beta1,2))+" "+str(round(regression(beta0,beta1),2)))


def compute_betas():
    data=get_dataset()
    sum=0
    sum2=0
    for i in data:
        sum=sum+i[0]
        sum2=sum2+i[1]
    meanx=sum/len(data)
    meany=sum2/len(data)
    sump=0
    divider=0
    for j in data:
        sump=sump+(j[0]-meanx)*(j[1]-meany)
        divider=divider+(j[0]-meanx)**2
    beta1=sump/divider
    beta0=meany-beta1*meanx
    return (beta0,beta1,regression(beta0,beta1))


def predict(year):
    x=compute_betas()
    return x[0]+x[1]*year


def iterate_normalized(T, eta):
    beta0 = 0
    beta1 = 0
    for i in range(1, T + 1):
        beta0 = beta0 - eta * (normal_grad(beta0, beta1)[0])
        beta1 = beta1 - eta * (normal_grad(beta0, beta1)[1])
        print(str(i) + " " + str(round(beta0, 2)) + " " + str(round(beta1, 2)) + " " + str(round(norm_regression(beta0, beta1), 2)))


def s_grad(beta_0,beta_1):
    data = get_dataset()
    sum = 0
    for p in data:
        sum = sum + p[0]
    mean = sum / len(data)
    import statistics
    tocal = []
    for au in data:
        tocal.append(au[0])
    std = statistics.stdev(tocal)
    for o in range(len(data)):
        data[o][0] = (data[o][0] - mean) / std
    import random
    randomx=random.choice(data)[0]
    randomy=random.choice(data)[1]
    return (2*(beta_0+beta_1*randomx-randomy),2*(beta_0+beta_1*randomx-randomy)*randomx)


def sgd(T, eta):
    beta0 = 0
    beta1 = 0
    for i in range(1, T + 1):
        beta0 = beta0 - eta * (s_grad(beta0, beta1)[0])
        beta1 = beta1 - eta * (s_grad(beta0, beta1)[1])
        print(str(i) + " " + str(round(beta0, 2)) + " " + str(round(beta1, 2)) + " " + str(round(norm_regression(beta0, beta1), 2)))
