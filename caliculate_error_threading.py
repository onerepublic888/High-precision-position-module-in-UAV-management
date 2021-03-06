import threading
import numpy as np
import sys, os, json, collections, time



def cal_error(D2, gt_dis):
    A = np.array([[1,1,0,0],[1,0,1,0],[1,0,0,1],[0,1,1,0],[0,1,0,1],[0,0,1,1]])
    lsq_A = np.dot(np.linalg.inv(np.dot(A.T, A)),(A.T))
    gt_dis = np.array(gt_dis)
    if (len(D2) != 6):
        raise ValueError('Distance array not right!')
    D2_raw = D2
    D2 = np.mean(D2, axis = 1)
    error = np.dot(lsq_A, (D2 - gt_dis))/6
    np.savez('UWB_cali_data.npz', D2_raw = D2_raw, D2 = D2, gt_dis = gt_dis, error = error)
    
    return error

def cal_Anc_pos(dis):#d01, d02, d03, d12, d13, d23 uncounterclockwise,with a0,a1,a2=>z=0, z3=>z != 0
    dis = np.array(dis)
    a0, a1 = [0, 0, 0], [dis[0], 0, 0]   
    x2 = round((dis[0]**2 + dis[1]**2 - dis[3]**2)/2*dis[0], 2)     # x2 = (d01**2+d02**2-d12**2)/2d01
    y2 = round((abs(dis[1]**2 - x2**2))**0.5, 2)                    #y2 = (d02**2 - x2**2)*0.5
    a2 = [x2, y2, 0]  
    x3 = round((dis[0]**2 + dis[2]**2 - dis[4]**2)/2*dis[0], 2)     # 
    y3 = round((y2/2 - (dis[2]**2 - dis[5]**2 - x2*(2*x3 - x2))/2*y2), 2)   #
    if ((dis[2]**2 - x3**2 - y3**2) > 0):
        z3 = round((abs(dis[2]**2 - x3**2 - y3**2))**0.5, 2)        #
    else:
        z3 = 0
    a3 = [x3, y3, z3]
    
    anc_pos = [a0, a1, a2, a3]
    return anc_pos
   
def remove_dis_err(original_dis):
    data = np.load('UWB_cali_data.npz')
    original_dis = np.array(original_dis)
    UWB_err = data['error']
    new_dis = original_dis - UWB_err
    
    return new_dis