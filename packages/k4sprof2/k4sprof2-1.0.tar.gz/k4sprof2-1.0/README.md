# for k4s profile.

## requires
- os
- time
- torch
- logging
- pandas
- torchstat

## profile content
- stage time
- model params、flops、memrw

## install
``` 
pip isntall -r requirement.txt
pip install k4sprof
```
## quick start
``` 
import k4sprof
prof = k4sprof.Prof(10, 30)
prof.profit(model, (3, 224, 224))
for step, data in enumerate(trainloader):
    prof.timeit(step, 'data load') #data
    inputs, labels = data[0].cuda(), data[1].cuda(); prof.timeit(step, 'h2d') #h2d
    outputs = model(inputs); prof.timeit(step, 'forward') #forward
    loss = criterion(outputs, labels); prof.timeit(step, 'loss') #loss
    optimizer.zero_grad(); prof.timeit(step, 'zero grad') #zero grad
    loss.backward(); prof.timeit(step, 'backward') #backward
    optimizer.step(); prof.timeit(step, 'optim') #optim
```