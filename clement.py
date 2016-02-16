from heapq import *
from math import sqrt

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
ol=[(-1,-1,-1,[]) for i in range(o)]
for i in range(o):
	a,b=map(int,input().split())
	nb=int(input())
	l=[int(j) for j in input().split()]
	v=[0 for j in range(p)]
	for x in l:
		v[x]+=1
	ol[i]=(a,b,v)

pq=[]
for i in range(d):
	heappush(pq,(0,i,wl[0][0],wl[0][1]))

needed=[0 for i in range(p)]
for _,_,v in ol:
	for j in range(p):
		needed[j]+=v[j]

load=[[0 for j in range(p)] for i in range(d)]

def warehouse(a,b):
	i=-1
	for x,y,_ in wl:
		i+=1
		if x==a and y==b:
			return(i)
	return(-1)

def puissance_warehouse(i,a,b):
	x,y,l=wl[i]
	nb=0
	for j in range(p):
		nb+=min(l[j],needed[j])
	dist=round(sqrt((a-x)**2+(b-y)**2))
	return(nb/dist)

def best_warehouse(a,b):
	best=-1
	puissance=-1
	for i in range(w):
		puissance_temp=puissance_warehouse(i,a,b)
		if puissance_temp>puissance:
			best=i
			puissance=puissance_temp
	return(best)

def best_client(nd,a,b):
	bx=-1
	by=-1
	nbb=-1
	for i in range(o):
		nb=0
		x,y,v=ol[i]
		for j in range(p):
			nb+=min(load[nd][j],v[j])
		if nb>nbb and x*y!=a*b:
			nbb=nb
			bx=x
			by=y
	return(bx,by)
	
def client_in(nd,a,b):
	for i in range(o):
		x,y,_=ol[i]
		if x==a and y==b and nb_deliver_client(nd,i)>0:
			return(i)
	return(-1)

def nb_deliver_client(nd,i):
	nb=0
	_,_,v=ol[i]
	for j in range(p):
		nb+=min(load[nd][j],v[j])
	#print('nb deliver',nd,i,nb)
	return(nb)

def deliver_client(nd,client,tt):
	global com,nb_com
	x,y,v=ol[client]
	nb_max=-1
	item=-1
	for j in range(p):
		nb=min(load[nd][j],v[j])
		if nb>nb_max:
			nb_max=nb
			item=j
	com+=str(nd)+' D '+str(client)+' '+str(item)+' '+str(nb_max)+'\n'
	nb_com+=1
	load[nd][item]-=nb_max
	v[item]-=nb_max
	ol[client]=(x,y,v)

def load_best(nd,ware):
	global com,nb_com
	nb=0
	free=pds
	x,y,l=wl[ware]
	for poids,i in plt:
		u=min(min(free//poids,needed[i]),l[i])
		if u>0:
			free-=u*poids
			com+=str(nd)+' L '+str(ware)+' '+str(i)+' '+str(u)+'\n'
			nb_com+=1
			load[nd][i]+=u
			needed[i]-=u
			l[i]-=u
			nb+=1
	wl[ware]=(x,y,l)
	return(nb)

t=3000
com=""
nb_com=0

while(True):
	tt,nd,a,b=heappop(pq)
	if tt>=t:break
	
	ware=warehouse(a,b)
	if sum(load[nd])!=0:
		#print('a')
		client=client_in(nd,a,b)
		nb=0
		if client>=0:nb=nb_deliver_client(nd,client)
		if nb<=0:
			x,y=best_client(nd,a,b)
			dist=round(sqrt((a-x)**2+(b-y)**2))
			heappush(pq,(tt+dist,nd,x,y))
		else:
			deliver_client(nd,client,tt)
			heappush(pq,(tt+1,nd,a,b))
	elif ware==-1:
		#print('b')
		ware=best_warehouse(a,b)
		x,y,_=wl[ware]
		dist=round(sqrt((a-x)**2+(b-y)**2))
		heappush(pq,(tt+dist,nd,x,y))
	else:
		#print('c')
		nb=load_best(nd,ware)
		heappush(pq,(tt+nb,nd,a,b))		

print(nb_com)
print(com)
	
