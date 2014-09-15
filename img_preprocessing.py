#filename:img_processing.py
import glob
import sys
from PIL import Image
from numpy import *
import numpy as np

def get_training_data(path,pixels):
  search_jpg=path+'/*.jpg'
  files=glob.glob(search_jpg)
  data_Matrix=[[0 for y in range(pixels)]for x in range(len(files))]
  m=0
  for fn in files:
    img=Image.open(fn)
    seq=get_img_data(img)
    data_Matrix[m]=seq
    m+=1
  return data_Matrix

def img_scaling(img):
  scale=0.0
  if not isinstance(img,Image.Image):
    img=Image.open(img)
  img=img.convert('L')
  if (img.size[0]>320):
    scale=float(320)/float(img.size[0])
    img=img.resize((int(img.size[0]*scale),int(img.size[1]*scale)))
  return img

def mean_normalization(training_data,dimension):
  u=[0 for j in range(dimension)]
  temp=[0 for j in range(dimension)]
  for i in range(len(training_data)):
      for j in range(dimension):
        temp[j]+=training_data[i][j]
  for j in range(dimension):
    u[j]=int(temp[j]/len(training_data))
  for i in range(len(training_data)):
    for j in range(dimension):
      training_data[i][j]-=u[j]
  return training_data

def get_img_data(img):
  if not isinstance(img,Image.Image):
    img=Image.open(img)
  seq=list(img.getdata())
  return seq


def cov_matrix(training_data,dimension):
    m_Matrix=[[0 for y in range(dimension)] for x in range(dimension)]
    m=0
    for seq in training_data:
        o_seq=np.array(seq)
        o_seq.shape=(dimension,1)
        t_seq=np.transpose(o_seq)
        m_Matrix=np.dot(o_seq,t_seq)
        m+=1
    return m_Matrix/m

def reduce_u(m_Matrix,dimension,k):
    u,sigma,vt=linalg.svd(m_Matrix)
    resig=[[0 for i in range(k)]for i in range(k)]
    for i in range(k):
        resig[i][i]=sigma[i]
    resig=mat(resig)
    print ''
    print 'the k dimension sigma matrix:'
    print ''
    print resig 
    print ''
    print 'the original data matrix:'
    print ''
    print u[:,:k]*resig*vt[:k,:]
    t_Matrix=np.array(m_Matrix)
    u_Reduce=np.array(u[:,:k])
    sk=0.0
    sn=0.0
    for i in range(k):
        sk+=sigma[i]
    for n in range(dimension):
        sn+=sigma[n]
    variance=round(float((sk/sn)*100),3)
    print ''
    print '%f percent of variance is retained' % variance
    print ''
    return u_Reduce

def reduce_matrix(training_data,reduce_u):
    return np.dot(reduce_u.T,np.array(training_data).T)

if __name__=='__main__':
  if len(sys.argv)!=2:
    print 'Usage:%s Training image path' % sys.argv[0]
  else:
    TrainingData=get_training_data(sys.argv[1],400)
    TrainingData=mean_normalization(TrainingData,400)
    c_Matrix=cov_matrix(TrainingData,400)
    r_u=reduce_u(c_Matrix,400,2)
    print 'the k dimension data matrix:'
    print ''
    print reduce_matrix(TrainingData,r_u)
