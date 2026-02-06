#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import cv2


# In[2]:


def choosep():
    i = random.randint(0,num-1)
    j = random.randint(0,num-1)
    newp = np.array([i,j])
    return newp


# In[3]:


def randwalk(num,curr):
    while 1:
        i = random.randint(1,4)
        if(curr[1]==0):
            if(i==3):
                continue
        if(curr[1]==num-1):
            if(i==4):
                continue
        if(curr[0]==0):
            if(i==1):
                continue
        if(curr[0]==num-1):
            if(i==2):
                continue


        if (i == 1):

            return np.array([-1,0])+curr
        elif (i ==2):

            return np.array([1,0])+curr
        elif(i == 3):

            return np.array([0,-1])+curr
        elif(i == 4):

            return np.array([0,1])+curr


# In[4]:


def changeval(grid,point,k):
    grid[point[0]][point[1]]=k


# In[5]:


def vali(grid,point):
    if(grid[point[0]][point[1]]==1):
        return False
    elif(grid[point[0]][point[1]]==0):
        return True


# In[6]:


def dismantle(p,edges,way):
    edges[p[0]][p[1]][way]=0
    #way: 1 is up,2 is down, 3 is left, 4 is right


# In[7]:


def breakwall(p1,p2,edges):
    dy=p2[0]-p1[0]
    dx=p2[1]-p1[1]
    if dx==1:
        dismantle(p1,edges,4)
        dismantle(p2,edges,3)
    elif(dx==-1):
        dismantle(p1,edges,3)
        dismantle(p2,edges,4)
    elif(dy==-1):
        dismantle(p1,edges,1)
        dismantle(p2,edges,2)
    elif(dy==1):
        dismantle(p1,edges,2)
        dismantle(p2,edges,1)





# In[8]:


def drawmaze(grid,edges,cell=30,wall=2):
    n=grid.shape[0]
    H = n*cell
    W=n*cell
    img=np.zeros((H,W,3),dtype=np.uint8)
    white = (255, 255, 255)
    grey  = (120, 120, 120)
    black = (0, 0, 0)
    color= (24,48,94)
    for i in range(n):
        for j in range(n):
            x=j*cell
            y=i*cell
            if (grid[i][j]==2):
                cv2.rectangle(img,(x,y),(x+cell,y+cell),grey,-1)
            elif(grid[i][j]==1):
                cv2.rectangle(img,(x,y),(x+cell,y+cell),white,-1)
            if (edges[i][j][1]==1 and i!=0):
                cv2.line(img,(x,y),(x+cell,y),color,wall)
            if(edges[i][j][3]==1 and j!=0):
                cv2.line(img,(x,y),(x,y+cell),color,wall)
    return img



# In[ ]:


num = 15
grid = np.zeros((num,num),dtype=int)
edges = np.ones((num,num,5),dtype=int)
startp = np.array([1,1])
changeval(grid,startp,1)
img=drawmaze(grid,edges)
cv2.imshow("mymaz",img)

while not np.all(grid==1):#before filled

    newp = choosep()
    if not(vali(grid,newp)):
        continue
    else:



        #from here init no problem.


        curr=newp.copy()
        paths=[curr.copy()]#a list of dots(curr)
        while True:
            #walk
            while(grid[curr[0]][curr[1]]==0):# attatch wrong then again

                changeval(grid,curr,2)

                img=drawmaze(grid,edges)
                cv2.imshow("mymaz",img)
                cv2.waitKey(1)
                curr=randwalk(num,curr)
                paths.append(curr.copy())

           #determine
            if(grid[curr[0]][curr[1]]==2):
                #wrong
                loop_begin=None
                for index,p in enumerate(paths):
                    if(p==curr).all():
                        loop_begin=index
                        break
                for p in paths[loop_begin+1:]:
                    grid[p[0]][p[1]]=0
                    img=drawmaze(grid,edges)
                    cv2.imshow("mymaz",img)
                    cv2.waitKey(1)
                paths=paths[:loop_begin+1]
                curr=paths[-1]

                continue
            elif(grid[curr[0]][curr[1]]==1):
                #right
                for p in paths:
                    grid[p[0]][p[1]]=1
                    img=drawmaze(grid,edges)
                    cv2.imshow("mymaz",img)
                    cv2.waitKey(1)
                for i in range(len(paths)-1):
                    p1=paths[i]
                    p2=paths[i+1]
                    breakwall(p1,p2,edges)
                    img=drawmaze(grid,edges)
                    cv2.imshow("mymaz",img)
                    cv2.waitKey(1)

                break
cv2.waitKey(0)
cv2.destroyAllWindows()








# In[ ]:





