from heapq import *
from math import sqrt,ceil
import sys

r,c,d,t,pds=map(int,input().split())
p=int(input())
pl=[int(i) for i in input().split()]
plt=[(pl[i],i) for i in range(p)]
plt.sort()
w=int(input())
wl=[(-1,-1,[]) for i in range(w)]
for i in range(w):
    a,b=map(int,input().split())
    l=[int(j) for j in input().split()]
    wl[i]=(a,b,l)
o=int(input())
ol=[(-1,-1,[]) for i in range(o)]
for i in range(o):
    a,b=map(int,input().split())
    nb=int(input())
    l=[int(j) for j in input().split()]
    v=[0 for j in range(p)]
    for j in l:
        v[j]+=1
    ol[i]=(a,b,v)

def dist(a,b,x,y):
    return(ceil(sqrt((a-x)**2+(b-y)**2)))
    
pq_drone=[]
for i in range(d):
    heappush(pq_drone,(0,i,wl[0][0],wl[0][1]))

pq_order=[]
for i in range(o):
    weight=0
    _,_,l=ol[i]
    for j in l:
        weight+=pl[j]
    heappush(pq_order,(weight,i))

current=-1
order_x=-1
order_y=-1
order_l=[]

nb_com=0
com=""
nnb=0
#t=200

xx=sum(wl[0][2])

while(True):
    tt,nd,a,b=heappop(pq_drone)
    # print("Drone :",nd,file=sys.stderr)
    # print("Time :",tt,file=sys.stderr)
    if tt>=t:break
    
    if current==-1:
        if pq_order==[]:
            break
        _,current=heappop(pq_order)
        order_x,order_y,order_l=ol[current]
        # print("Order :",current,file=sys.stderr)
        
    order_list=[]
    for i in range(p):
        for j in range(order_l[i]):
            order_list+=[i]
        
    ware_best=-1
    maxi=-1
    dist_best=-1
    load_best=[-1 for i in range(p)]
    for ware in range(w):
        # print("   Warehouse :",ware,end=" ",file=sys.stderr)
        weight=0
        load_temp=[0 for i in range(p)]
        ware_x,ware_y,_=wl[ware]
        ware_list=[wl[ware][2][produit] for produit in range(p)]
        for produit in order_list:
            #if ware_list[produit]>0:print("yolo",end=" ",file=sys.stderr)
            if ware_list[produit]>0 and weight+pl[produit]<=pds:
                weight+=pl[produit]
                ware_list[produit]-=1
                load_temp[produit]+=1
        dist_temp=dist(a,b,ware_x,ware_y)+dist(ware_x,ware_y,order_x,order_y)
        #print(weight,dist_temp,file=sys.stderr)
        score=(1000*weight)/dist_temp
        if score>maxi:
            maxi=score
            ware_best=ware
            dist_best=dist_temp
            for i in range(p):
                load_best[i]=load_temp[i]
    
    if score==0.0:
        current=-1
        nnb+=1
        # print("bye bye",sum(wl[0][2]),order_list,file=sys.stderr)
        heappush(pq_drone,(tt,nd,a,b))
    else:
    
        wait=dist_best
        ware_x,ware_y,ware_list=wl[ware_best]
        com2=""
        for produit in range(p):
            if load_best[produit]>0:
                nb_com+=2
                # print(str(nd)+" L "+str(ware_best)+" "+str(produit)+" "+str(load_best[produit]),file=sys.stderr)
                # print(str(nd)+" D "+str(current)+" "+str(produit)+" "+str(load_best[produit]),file=sys.stderr)
                com+=str(nd)+" L "+str(ware_best)+" "+str(produit)+" "+str(load_best[produit])+"\n"
                com2+=str(nd)+" D "+str(current)+" "+str(produit)+" "+str(load_best[produit])+"\n"
                wait+=2
                ware_list[produit]-=load_best[produit]
                order_l[produit]-=load_best[produit]
                    
        com+=com2
        heappush(pq_drone,(tt+wait,nd,order_x,order_y))
                    
        if sum(order_l)==0:
            current=-1
        
yy=sum(wl[0][2])
        
print(nb_com)
print(nb_com,file=sys.stderr)
print(com,end="")
# print(com,file=sys.stderr)
# print(nnb,o,file=sys.stderr)
# print(xx,yy,file=sys.stderr)