#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import cv2
import random
ANI_FULL = 1
ANI_FAST = 2
ANI_RATIO = 3
ANI_NONE = 4

class wilsonmaze:
    EMPTY = 0
    TREE = 1
    WALK = 2
    def __init__(self,num,ratio,ani_mode):
        self.num=num
        self.grid=np.zeros((num,num),dtype=int)
        self.edges=np.ones((num,num,5),dtype=int)
        self.road_amount=0
        self.ratio=ratio
        self.ani_mode=ani_mode
        self.count=0
        self.delay=10

    def draw(self,cell=30,wall=2):
        grid=self.grid
        edges = self.edges
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
                if (grid[i][j]==self.WALK):
                    cv2.rectangle(img,(x,y),(x+cell,y+cell),grey,-1)
                elif(grid[i][j]==self.TREE):
                    cv2.rectangle(img,(x,y),(x+cell,y+cell),white,-1)
                if (edges[i][j][1]==1 and i!=0):
                    cv2.line(img,(x,y),(x+cell,y),color,wall)
                if(edges[i][j][3]==1 and j!=0):
                    cv2.line(img,(x,y),(x,y+cell),color,wall)
        return img


    def drawmaze(self,new_status=None,force=False):
        if force is True:
            img = self.draw()
            cv2.imshow("mymaze",img)
            cv2.waitKey(100)
            return
        if new_status is None:
            new_status=self.EMPTY
        if self.ani_mode == ANI_NONE:
            return
        if self.ani_mode == ANI_RATIO:
            self.count += 1
            if(self.count%self.ratio==0):
                img=self.draw()
                cv2.imshow("mymaze",img)
                cv2.waitKey(self.delay)

                return
        if self.ani_mode == ANI_FAST:
            if new_status == self.TREE:#only draw tree,no seek
                img=self.draw()
                cv2.imshow("mymaze",img)
                cv2.waitKey(1)
                return

        if self.ani_mode == ANI_FULL:
            img = self.draw()
            cv2.imshow("mymaze",img)
            cv2.waitKey(1)
            return





    def changeval(self,curr,k):
        self.grid[curr[0]][curr[1]]=k


    def dismantle(self,p,way):
        self.edges[p[0]][p[1]][way]=0
        #way: 1 is up,2 is down, 3 is left, 4 is right
    def breakwall(self,p1,p2):
        dy=p2[0]-p1[0]
        dx=p2[1]-p1[1]
        if dx==1:
            self.dismantle(p1,4)
            self.dismantle(p2,3)
        elif(dx==-1):
            self.dismantle(p1,3)
            self.dismantle(p2,4)
        elif(dy==-1):
            self.dismantle(p1,1)
            self.dismantle(p2,2)
        elif(dy==1):
            self.dismantle(p1,2)
            self.dismantle(p2,1)


    def choosep(self):
        i = random.randint(0,self.num-1)
        j = random.randint(0,self.num-1)
        newp = np.array([i,j])
        return newp


    def vali(self,point):
        if(self.grid[point[0]][point[1]]==self.TREE):
            return False
        elif(self.grid[point[0]][point[1]]==self.EMPTY):
            return True


    def randwalk(self,curr):
        while True:
            i = random.randint(1,4)
            if(curr[1]==0):
                if(i==3):
                    continue
            if(curr[1]==self.num-1):
                if(i==4):
                    continue
            if(curr[0]==0):
                if(i==1):
                    continue
            if(curr[0]==self.num-1):
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


    def generate_step(self,curr,paths):
        while True:


                while(self.grid[curr[0]][curr[1]]==self.EMPTY):
                    self.changeval(curr,self.WALK)
                    self.drawmaze()

                    curr=self.randwalk(curr)
                    paths.append(curr.copy())
                    #determine
                    if(self.grid[curr[0]][curr[1]]==self.WALK):
                        #wrong
                        loop_begin=None
                        for index,p in enumerate(paths):
                            if (p==curr).all():
                                loop_begin=index
                                break
                        for p in paths[loop_begin+1:]:
                            self.grid[p[0]][p[1]]=self.EMPTY
                            self.drawmaze()
                        paths=paths[:loop_begin+1]
                        curr=paths[-1]
                        continue
                    elif(self.grid[curr[0]][curr[1]]==self.TREE):

                        for p in paths:
                            self.grid[p[0]][p[1]]=self.TREE
                            self.drawmaze(self.TREE)
                        for i in range(len(paths)-1):
                            p1=paths[i]
                            p2=paths[i+1]
                            self.breakwall(p1,p2)
                            self.drawmaze()
                break
    def generate(self):
        self.grid[1][1]=self.TREE
        while not np.all(self.grid==self.TREE):#before filled
            newp = self.choosep()
            if not(self.vali(newp)):
                continue


            curr=newp.copy()
            paths=[curr.copy()]
            #init completed
            self.generate_step(curr,paths)
        self.drawmaze(force=True)  














maze = wilsonmaze(
    num = 30,
    ratio = 90,
    ani_mode=ANI_RATIO
)

maze.generate()




# In[ ]:





# In[ ]:





# In[ ]:




