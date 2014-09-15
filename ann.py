#filename:ann.py
import random
from math import exp
from math import log

dBias=1

class SNeuron:
  def __init__(self,NumInputs):
    self.NumInputs=NumInputs+1
    self.m_vecWeight=[]
    for x in range(self.NumInputs):
      self.m_vecWeight.append(float('%.2f'%random.uniform(-1,1)))
  def info(self):
    print 'The number of input is %d' % self.NumInputs
  def OutputWeight(self):
    for i in self.m_vecWeight:
      print i

class SNeuronLayer:
  def __init__(self,NumNeurons,NumInputsPerNeuron):
    self.NumNeurons=NumNeurons
    self.NumInputsPerNeuron=NumInputsPerNeuron
    self.m_vecNeurons=[]
    for i in range(self.NumNeurons):
      self.m_vecNeurons.append(SNeuron(self.NumInputsPerNeuron))
  def info(self):
    print 'The Number of Nueron is %d' % self.NumNeurons
    print 'The number of input per Nueron is %d' % self.NumInputsPerNeuron

class SNeuralNet:
  def __init__(self):
    self.m_NumInputs=2
    self.m_NumOutputs=1
    self.m_NumOfHiddenLyrs=1
    self.m_NeuronsPerHiddenLyr=2
    self.mVecLayer=[]
    self.OutputOfEveryLyr=[]
    self.cost=0
  def CreateNet(self):
    if(self.m_NumOfHiddenLyrs>0):
      self.mVecLayer.append(SNeuronLayer(self.m_NeuronsPerHiddenLyr,self.m_NumInputs))
      for i in range(self.m_NumOfHiddenLyrs-1):
        self.mVecLayer.append(SNeuronLayer(self.m_NeuronsPerHiddenLyr,self.m_NeuronsPerHiddenLyr))
      self.mVecLayer.append(SNeuronLayer(self.m_NumOutputs,self.m_NeuronsPerHiddenLyr))
    else:
      self.mVecLayer.append(SNeuronLayer(self.m_NumOutputs,self.m_NumInputs))
      self.mVecLayer[0].m_vecNeurons[0].OutputWeight()
  def activate(self,m_input):
      self.OutputOfEveryLyr=[]
      output=[]
      cWeight=0
      if(len(m_input)!=self.m_NumInputs):
        return output
      for i in range(self.m_NumOfHiddenLyrs+1):
        if(i>0):
          m_input=output
          self.OutputOfEveryLyr.append(output)
          #for x in m_input:
            #print x
        output=[]
        cWeight=0
        for j in range(self.mVecLayer[i].NumNeurons):
          NetInput=0
          cWeight=0
          NumInputs=self.mVecLayer[i].m_vecNeurons[j].NumInputs
          for k in range(NumInputs-1):
            NetInput+=self.mVecLayer[i].m_vecNeurons[j].m_vecWeight[k]*m_input[cWeight]
            cWeight+=1
          NetInput+=self.mVecLayer[i].m_vecNeurons[j].m_vecWeight[self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]*dBias
          output.append(round(self.sigmoid(NetInput),3))
      print 'The output is %.2f' % output[0]
      return output
  def sigmoid(self,activation):
    return round(1/(1+round(exp(-activation),3)),3)

  def costFunction(self,DataSet):
    temp_cost=0.0
    for data in DataSet:
      activation=self.activate(data[0])
      temp_cost=round(temp_cost+data[1]*round(log(activation[0]),3)+(1-data[1])*round(log(1-activation[0]),3),3)
    self.cost=round(temp_cost/(-len(DataSet)),3)
    return self.cost

  def BackPropagation(self,TrainingData,learningRate):
    if(self.m_NumOfHiddenLyrs==0):
      temp=[[0 for col in range(self.m_NumInputs+1)] for row in range(self.m_NumOfHiddenLyrs+1)]
      descent=[[0 for col in range(self.m_NumInputs+1)] for row in range(self.m_NumOfHiddenLyrs+1)]
    else:
      temp=[[[0.0 for z in range(self.m_NeuronsPerHiddenLyr+1)] for col in range(self.m_NeuronsPerHiddenLyr+1)]for row in range(self.m_NumOfHiddenLyrs)]
      descent=[[[0.0 for z in range(self.m_NeuronsPerHiddenLyr+1)] for col in range(self.m_NeuronsPerHiddenLyr+1)]for row in range(self.m_NumOfHiddenLyrs)]
      m_vecError=[[0.0 for col in range(self.m_NumInputs+1)] for row in range(self.m_NumOfHiddenLyrs)]
    for Training in TrainingData:
      activation=self.activate(Training[0])
      error=activation[0]-Training[1]
      print error
      if(self.m_NumOfHiddenLyrs==0):
          i=0
          for j in range(self.m_NumInputs):
            temp[i][j]=temp[i][j]+Training[i][j]*error
            print temp[i][j]
            if(j==self.m_NumInputs):
              descent[i][j]=round(temp[i][j]/(len(TrainingData)),3)
            else:
              descent[i][j]=round(temp[i][j]/(len(TrainingData))+learningRate*self.mVecLayer[0].m_vecNeurons[0].m_vecWeight[j],3)
              print descent[i][j]
      else:
          for i in range(self.m_NumOfHiddenLyrs):
            for j in range(self.mVecLayer[self.m_NumOfHiddenLyrs-i].NumNeurons):
              if(i==0):
                for k in range(self.mVecLayer[self.m_NumOfHiddenLyrs].m_vecNeurons[j].NumInputs-1):
                  m_vecError[self.m_NumOfHiddenLyrs-1][j]=round(self.mVecLayer[self.m_NumOfHiddenLyrs-1].m_vecNeurons[j].m_vecWeight[k]*error,3)
                  m_vecError[self.m_NumOfHiddenLyrs-1][self.mVecLayer[self.m_NumOfHiddenLyrs].m_vecNeurons[j].NumInputs-1]=round(self.mVecLayer[self.m_NumOfHiddenLyrs].m_vecNeurons[j].m_vecWeight[self.mVecLayer[self.m_NumOfHiddenLyrs].m_vecNeurons[j].NumInputs-1]*error,3)
                  temp[self.m_NumOfHiddenLyrs-1][j][0]=round(temp[self.m_NumOfHiddenLyrs-1][j][0]+self.OutputOfEveryLyr[self.m_NumOfHiddenLyrs-1][j]*error,3)
                  descent[self.m_NumOfHiddenLyrs-1][j][0]=round(temp[self.m_NumOfHiddenLyrs-1][j][0]/len(TrainingData)+learningRate*self.mVecLayer[self.m_NumOfHiddenLyrs-1].m_vecNeurons[j].m_vecWeight[k],3)
                  if(j==self.mVecLayer[self.m_NumOfHiddenLyrs-i].NumNeurons-1):
                    temp[self.m_NumOfHiddenLyrs-1][self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].NumInputs-1][0]=round(temp[self.m_NumOfHiddenLyrs-1][self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].NumInputs-1][0]+error,3)
                    descent[self.m_NumOfHiddenLyrs-1][self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].NumInputs-1][0]=round(temp[self.m_NumOfHiddenLyrs-1][self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].NumInputs-1][0]/len(TrainingData),3)
              else:
                for k in range(self.mVecLayer[i].m_vecNeurons[j].NumInputs-1):
                  m_vecError[self.m_NumOfHiddenLyrs-1-i][j]=round(m_vecError[self.m_NumOfHiddenLyrs-1-i][j]+self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight[k]*m_vecError[self.m_NumOfHiddenLyrs-i][j],3)
                  temp[self.m_NumOfHiddenLyrs-1-i][j][k]=round(temp[self.m_NumOfHiddenLyrs-1-i][j][k]+self.OutputOfEveryLyr[self.m_NumOfHiddenLyrs-1-i][j]*m_vecError[self.m_NumOfHiddenLyrs-i][k],3)
                  descent[self.m_NumOfHiddenLyrs-1-i][j][k]=round(temp[self.m_NumOfHiddenLyrs-1-i][j][k]/len(TrainingData)+learningRate*self.mVecLayer[self.m_NumOfHiddenLyrs-1-i].m_vecNeurons[j].m_vecWeight[k],3)
                  m_vecError[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]=round(m_vecError[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]+self.mVecLayer[self.m_NumOfHiddenLyrs-1-i].m_vecNeurons[j].m_vecWeight[self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]*m_vecError[self.m_NumOfHiddenLyrs-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1],3)
                  temp[self.m_NumOfHiddenLyrs-1-i][j][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]=round(temp[self.m_NumOfHiddenLyrs-1-i][j][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]+m_vecError[self.m_NumOfHiddenLyrs-i][j],3)
                descent[self.m_NumOfHiddenLyrs-1-i][j][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]=round(temp[self.m_NumOfHiddenLyrs-1-i][j][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1]/len(TrainingData),3)
          if(self.m_NumOfHiddenLyrs!=1):
            for k in range(self.mVecLayer[i].m_vecNeurons[j].NumInputs):
              temp[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1][k]=round(temp[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1][k]+m_vecError[self.m_NumOfHiddenLyrs-i][k],3)
              descent[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1][k]=round(temp[self.m_NumOfHiddenLyrs-1-i][self.mVecLayer[i].m_vecNeurons[j].NumInputs-1][k]/len(TrainingData),3)
    return descent
  def gradient_descent(self,TrainingData,learningrate,iteration,cost_threshold):
    m=0
    cost=0
    while(m<iteration):
      descent=self.BackPropagation(TrainingData,learningrate)
      for i in range(self.m_NumOfHiddenLyrs):
        for j in range(self.mVecLayer[self.m_NumOfHiddenLyrs-i].NumNeurons):
          for k in range(self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].NumInputs):
            print self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight
            print self.OutputOfEveryLyr[self.m_NumOfHiddenLyrs-1-i]
            if (i==0):
              self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight[k]=round(self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight[k]-descent[self.m_NumOfHiddenLyrs-1-i][j][0],3)
            else:
              self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight[k]=round(self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight[k]-descent[self.m_NumOfHiddenLyrs-1-i][j][k],3)
            print self.mVecLayer[self.m_NumOfHiddenLyrs-i].m_vecNeurons[j].m_vecWeight
      cost=self.costFunction(TrainingData)
      m+=1
      if (abs(cost)<=cost_threshold):
        print abs(cost)
        break


my_NeuralNet=SNeuralNet()
my_NeuralNet.CreateNet()
my_NeuralNet.gradient_descent([[[9.28821749e+02,7.65970116e+00],1],[[-9.30089243e+02,1.52794597e-02],1]],0.01,10000,0.01)


