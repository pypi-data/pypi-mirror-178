import random
import copy
import math
import numpy as np

    
class nn:
    def __init__(self,layers:list,weightDomain:tuple=(-1,1),biasDomain:tuple=(-0.1,0.1)) -> None:
        self.layers=layers
        self.weight={}
        self.bias=[]

        for i in range(len(layers)-1):
            for i2 in range(layers[i]):
                for i3 in range(layers[i+1]):
                    self.weight[f"{i}.{i2}:{i+1}.{i3}"]=random.uniform(*weightDomain)
        for i in range(len(layers)-1):
            tmp=[]
            for i2 in range(layers[i+1]):
                c=random.uniform(*biasDomain)
                tmp.append(c)
                #self.bias[f"{i+1}.{i2}"]=
            self.bias.append(tmp)
    def set(self,w,b):
        self.bias=copy.deepcopy(b)
        self.weight=copy.copy(w)
    def forward(self,inp:list,activations:list=None):
        if activations==None:
            del activations
            def activation(x):return x
            activations=[activation for i in range(len(self.layers)-1)]
            del activation
        self.activations=activations
        add=copy.deepcopy(self.bias)
        layers=[inp]+add
        del add
        l=copy.deepcopy(layers)
        for i in range(len(self.layers)-1):
            for i2 in range(self.layers[i]):
                for i3 in range(self.layers[i+1]):
                    layers[i+1][i3]+=(layers[i][i2]*self.weight[f"{i}.{i2}:{i+1}.{i3}"])

                l[i+1][i3]=self.activations[i](layers[i+1][i3])
                
        return l[-1]

def crossover(a,b,mutation:float=0,n:int=1,):
    def crossoverOne(a,b,mutation):
        modelA=copy.deepcopy(a)
        modelB=copy.deepcopy(b)
        
        #bias crossover
        newModelBias=[]
        for i in range(len(modelA.bias)):
            tmp=[]
            for i2 in range(len(modelA.bias[i])):
                
                th= random.randint(0,2)
                if th==0:tmp.append(modelA.bias[i][i2])
                if th==1:tmp.append(modelB.bias[i][i2])
                if th==2:tmp.append((modelA.bias[i][i2]+modelB.bias[i][i2])/2)
                if mutation>random.random():
                    tmp[-1]=random.uniform(-tmp[-1]*2,tmp[-1]*2)
            newModelBias.append(tmp)
        #weight crossover
        newModelWeight={}
        for key in modelA.weight.keys():
            th= random.randint(0,2)
            if th==0:newModelWeight[key]= modelA.weight[key]
            if th==1:newModelWeight[key]= modelB.weight[key]
            if th==2:newModelWeight[key]= (modelA.weight[key]+modelB.weight[key])/2
        m=nn(modelA.layers)
        m.set(newModelWeight,newModelBias)
        return m
    if n==1:
        return crossoverOne(a,b,mutation)
    else:
        return [crossoverOne(a,b,mutation) for _ in range(n)]


#def manynn(layers:list,n:int) ->list:
#    return [nn(layers) for _ in range(n)]
#def multipleForward(models:list,inp:list):
#    return [_.forward(inp) for _ in models]