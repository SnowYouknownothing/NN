# -*- coding: utf-8 -*-
'''
Created on 2017年11月24日
@author: Administrator
'''
from numpy import random,exp,dot,eye
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
def sigmord(x):
    return 1/(1+exp(-x))
#     return 1.0-np.tanh(x)*np.tanh(x)
def error_output(o,t):
    return o*(1-o)*(t-o)
def PD(learning_rate,epochs,daying,x_input,y_output,index_hang,index_lie,layel):          
    w_im=2*random.random((layel[0],layel[1]))-1
    w_ml=2*random.random((layel[1],layel[2]))-1
    w_lk=2*random.random((layel[2],layel[3]))-1
    w_kj=2*random.random((layel[3],layel[4]))-1
    w_jo=2*random.random((layel[4],layel[5]))-1 
    b_m=2*random.random((layel[1],1))-1
    b_l=2*random.random((layel[2],1))-1
    b_k=2*random.random((layel[3],1))-1
    b_j=2*random.random((layel[4],1))-1
    b_o=2*random.random((layel[5],1))-1   
    less,i_x=[],[] 
    for j in range(epochs):
        number_suiji=random.randint(index_hang)
        x_input_suiji=eye(1,index_lie)
        for i in range(0,index_lie):
                x_input_suiji[0,i]=x_input[number_suiji,i]
#          x_input_suiji，（1,4） 
        y_output_suiji=y_output[number_suiji]
#         y_output_suiji，（1，1）
        l_m=dot(x_input_suiji,w_im)+ b_m.T
        sigmord_m=sigmord(l_m)
        
        l_l=dot(sigmord_m,w_ml)+ b_l.T
        sigmord_l=sigmord(l_l)
        l_k=dot(sigmord_l,w_lk)+ b_k.T
        sigmord_k=sigmord(l_k)
#            sigmord_k，（1,3）             
        l_j=dot(sigmord_k,w_kj)+ b_j.T
        sigmord_j=sigmord(l_j)
#            sigmord_j，（1,2）             
        l_o=dot(sigmord_j,w_jo)+b_o
        y_o=sigmord(l_o)
#            y_o，（1,1）         
        # 正向传播结束
        error_o=error_output(y_o,y_output_suiji)  
#         error_o(1,1)
        error_j=sigmord_j*(1-sigmord_j)*dot(error_o,(w_jo.T))
#         error_j(1,2)      
        error_k=sigmord_k*(1-sigmord_k) * dot(error_j,(w_kj.T))
#         error_k(1,3)      
        error_l=sigmord_l*(1-sigmord_l) * dot(error_k,(w_lk.T))
#         error_k(1,3)
        error_m=sigmord_m*(1-sigmord_m) * dot(error_l,(w_ml.T))
        
        w_im += dot(x_input_suiji.T,(learning_rate*error_m))       
        b_m += learning_rate*(error_m.T)
        w_ml += dot(sigmord_m.T,(learning_rate*error_l))       
        b_l += learning_rate*(error_l.T)
        w_lk += dot(sigmord_l.T,(learning_rate*error_k))        
        b_k += learning_rate*(error_k.T)
        w_kj+=dot(sigmord_k.T,learning_rate*error_j)
        b_j+=learning_rate*(error_j.T)
        w_jo+=learning_rate*error_o*(sigmord_j.T)
        b_o+=learning_rate*error_o
        
        i_x.append(j)
        less.append(float(y_o-y_output_suiji))
    if daying=='T':
        plt.figure(figsize=(100,100))
        plt.plot(i_x,less,label="$less$",color="red",linewidth=0.5)
        plt.ylim(-1,1)
        plt.xlabel("epochs")
        plt.ylabel("less")
        plt.legend()
        plt.show()
    return w_im,w_ml,w_lk,w_kj,w_jo,b_m,b_l,b_k,b_j,b_o

digits=load_digits()
x=digits.data
y=digits.target
x_input=x[:1000,:64]*0.1
y_output=y[:1000]*0.1
x_kaohe=x[1001:len(x),:64]*0.1
y_kaohe=y[1001:len(y)]*0.1

for i in range(1):
    index_hang,index_lie=len(x_input),len(x_input[0])
    epochs=10000
    learning_rate=4
    daying='T'
    m_index,j_index,k_index,l_index=40,40,40,40
    layel=[index_lie,m_index,l_index,k_index,j_index,1]  
    w_im,w_ml,w_lk,w_kj,w_jo,b_m,b_l,b_k,b_j,b_o = PD(
        learning_rate,epochs,daying,x_input,y_output,index_hang,index_lie,layel)
    zhunquelv,i_x1=[],[]
    zhengque1,zhengque2=0,0
    for j in range(len(y_kaohe)):
#         index_suiji=random.randint(len(y_kaohe)) 
        x_yuce=x_kaohe[j]
        y_ture=y_kaohe[j]
        x_input_suiji=eye(1,index_lie)
        for i in range(0,index_lie):
            x_input_suiji[0,i]=x_yuce[i]
        
#         y_output_suiji，（1，1）
        l_m=dot(x_input_suiji,w_im)+ b_m.T
        sigmord_m=sigmord(l_m)
        
        l_l=dot(sigmord_m,w_ml)+ b_l.T
        sigmord_l=sigmord(l_l)
        l_k=dot(sigmord_l,w_lk)+ b_k.T
        sigmord_k=sigmord(l_k)
#            sigmord_k，（1,3）             
        l_j=dot(sigmord_k,w_kj)+ b_j.T
        sigmord_j=sigmord(l_j)
#            sigmord_j，（1,2）             
        l_o=dot(sigmord_j,w_jo)+b_o
        y_o=sigmord(l_o)
            
        i_x1.append(j)
        if y_ture!=0.0:
#             print '第%s次预测数：%s，真实数为：%s，准确率为：%s'%(j+1,float(y_o),y_ture,x_zhunquelv)
            x_zhunquelv=float((y_o-y_ture)/y_ture)
            zhunquelv.append(x_zhunquelv)
#             print '第%s次预测数：%s，真实数为：%s，准确率为：%s'%(j+1,float(y_o),y_ture,x_zhunquelv)
        else:
#             print '第%s次预测数：%s，真实数为：%s'%(j+1,float(y_o),y_ture)
            zhunquelv.append(y_o)
        if y_o-y_ture>-0.05 and y_o-y_ture<0.05:
            zhengque1+=1
        if y_o-y_ture>-0.1 and y_o-y_ture<0.1:
            zhengque2+=1

    print '准确率百分之95以上的有%s个' %(zhengque1)
    print '准确率百分之90以上的%s个' %(zhengque2)
    plt.figure(figsize=(100,100))
    plt.plot(i_x1,zhunquelv,label="$zhunquelv$",color="red",linewidth=1)
    plt.ylim(-1,1)
    plt.xlabel("i_x1")
    plt.ylabel("zhunquelv")
    plt.legend()
    plt.show()
    
    plt.title("scatter diagram")
    plt.xlim(xmax=800,xmin=0)
    plt.ylim(ymax=1.5,ymin=-1)
    plt.xlabel("i_x1")
    plt.ylabel("zhunquelv")
    plt.scatter(i_x1,zhunquelv,s=5,alpha=0.9,marker='o')
    # plt.plot(i_x1,zhunquelv,'ro')   
    plt.show()
    
print'测试结束'







