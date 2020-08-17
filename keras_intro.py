import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras

def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    if training==False:
        return (test_images,test_labels)
    return (train_images,train_labels)

def print_stats(train_images,train_labels):
    print(len(train_images))
    print(str(len(train_images[0]))+"x"+str(len(train_images[0][0])))
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    for i in range(len(class_names)):
        count=0
        for j in train_labels:
            if j==i:
                count+=1
        print(str(i)+". "+class_names[i]+" - "+str(count))

def view_image(image,label):
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    a, b = plt.subplots(1, 1)
    x=b.imshow(image)
    a.colorbar(x, ax=b, fraction=0.046, pad=0.04)
    b.set_title(class_names[label])
    plt.show()
def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Input(shape=(28, 28)))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(10))
    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='Adam',
                  metrics=['accuracy'])
    return model

def train_model(model,images,labels,T):
    model.fit(images,labels,epochs=T)
    return model

def evaluate_model(model, images, labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(images, labels, verbose=0)
    if show_loss:
        print("Loss: " + str(round(test_loss, 2)))
    print("Accuracy: " + str("{0:.2%}".format(test_accuracy)))

def predict_label(model, images, index):
    model.add(keras.layers.Softmax())
    predictions = model.predict(images)[index]
    predi = predictions[:]
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    sorin = np.argpartition(predi, -3)[-3:]
    sorin2=[]
    for j in range(3):
        max = 0
        temp=sorin[0]
        for k in sorin:
            if predi[k]>max and k not in sorin2:
                max=predi[k]
                temp=k
        sorin2.append(temp)
    for i in range (3):
        print(str(class_names[sorin2[i]])+": "+str(format(predi[sorin2[i]],".2%")))



