if '__file__' in globals():
    import os,sys
    sys.path.append(os.path.join(os.path.expanduser(__file__),'..'))

import numpy as np
import dezero
from dezero.datasets import MNIST
from dezero.dataloaders import DataLoader
from dezero.models import MLP
from dezero.optimizers import SGD
import dezero.functions as F
import matplotlib.pyplot as plt

max_epochs=7
batch_size=100
lr=0.1
hidden_size=1000

train_set=MNIST(train=True)
test_set=MNIST(train=False)
train_loader=DataLoader(train_set,batch_size,shuffle=True)
test_loader=DataLoader(test_set,batch_size,shuffle=False)

model=MLP((hidden_size,10),activation=F.relu)
optimizer=SGD(lr=lr).setup(model)

train_losses,train_accs,test_losses,test_accs=[],[],[],[]
for epoch in range(max_epochs):
    sum_loss=0
    sum_acc=0
    sum_len=0
    for x,t in train_loader:
        y=model(x)
        loss=F.softmax_cross_entropy(y,t)

        model.cleargrads()
        loss.backward()
        optimizer.update()

        sum_loss+=float(loss.data)*len(t)
        acc=F.accuracy(y,t)
        sum_acc+=float(acc.data)*len(t)
        sum_len+=len(t)
    sum_loss/=sum_len
    sum_acc/=sum_len
    print('epoch %d'%(epoch+1))
    print('train loss:{:.2f},accuracy:{:.2f}'.format(sum_loss,sum_acc))
    train_losses.append(sum_loss)
    train_accs.append(sum_acc)

    with dezero.no_grad():
        sum_loss=0
        sum_acc=0
        sum_len=0
        for x,t in test_loader:
            y=model(x)
            loss=F.softmax_cross_entropy(y,t)
            acc=F.accuracy(y,t)

            sum_loss+=float(loss.data)*len(t)
            sum_acc+=float(acc.data)*len(t)
            sum_len+=len(t)
        sum_loss /= sum_len
        sum_acc /= sum_len
        print('test loss:{:.2f},accuracy:{:.2f}'.format(sum_loss, sum_acc))
        test_losses.append(sum_loss)
        test_accs.append(sum_acc)

plt.plot(train_losses,label='train')
plt.plot(test_losses,label='test')
plt.title('loss')
plt.legend()
plt.show()

plt.plot(train_accs,label='train')
plt.plot(test_accs,label='test')
plt.title('accuracy')
plt.legend()
plt.show()