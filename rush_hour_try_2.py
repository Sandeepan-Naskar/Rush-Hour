from z3 import *
import sys
import time

start_time = time.time()

s = Solver()

f = open(sys.argv[1], "r")

file=[]

for line in f.read().split():
    file.append([int(x) for x in line.split(',')])

board_size=file[0][0]
num_moves_max=file[0][1]

hor=[]
ver=[]

mines=[]

hor.append(file[1])
hor[0][1]=hor[0][1]+1

for arr in file:

    if(len(arr)==2):
        continue

    if(arr[0]==1):
        hor.append(arr[1::])
        #hor[-1][0]=hor[-1][0]-1
        hor[-1][1]=hor[-1][1]+1

    elif(arr[0]==0):
        ver.append(arr[1::])
        ver[-1][0]=ver[-1][0]+1
        #ver[-1][1]=ver[-1][1]-1
    else:
        mines.append(arr[1::])
        #mines[-1][0]-=1
        #mines[-1][1]-=1

######LOGIC BEGINS

#### Initialization

Mines=[None]*(len(mines))

for co in range(0,len(mines)):
    Mines[co] = Int('mine_%d' %(co))
    s.add(Mines[co]==(mines[co][0]*board_size+mines[co][1]))

Position_Horizontal = [[[None for _ in range(0,len(hor))] for _ in range(0,num_moves_max+1)] for _ in range(num_moves_max+1)]
Position_Vertical = [[[None for _ in range(0,len(ver))] for _ in range(0,num_moves_max+1)] for _ in range(num_moves_max+1)]

Moves=[None]*(num_moves_max)

for i in range(0,num_moves_max):
    Moves[i]=Int('moves_%d' %(i))

for i in range(0,len(hor)):
    Position_Horizontal[0][i]=Int('posh_%d_%d' %(0,i))
    s.add(Position_Horizontal[0][i]==(hor[i][0]*board_size+hor[i][1]))

for i in range(0,len(ver)):
    Position_Vertical[0][i]=Int('posv_%d_%d' %(0,i))
    s.add(Position_Vertical[0][i]==(ver[i][0]*board_size+ver[i][1]))

for i in range(1,num_moves_max+1):
    for j in range(0,len(hor)):
        Position_Horizontal[i][j]=Int('posh_%d_%d' %(i,j))


for i in range(1,num_moves_max+1):
    for j in range(0,len(ver)):
        Position_Vertical[i][j]=Int('posv_%d_%d' %(i,j))

for turn in range(0,num_moves_max):
    s.add(Moves[turn]<=2*(len(hor)+len(ver)))
    s.add(Moves[turn]>=0)



for turn in range(0,num_moves_max):
    
    ind=0

    for car in range(0,len(hor)):

        ### Forward Move

        Or_Predicate1=[None]*2

        Or_Predicate1[0] = Not(Moves[turn]==2*ind)

        And_Predicate1=[]

        #Boundary Condition
        
        #And_Predicate1.append((Position_Horizontal[turn][car])%board_size!=board_size-1)

        #Propagation

        for car2 in range(0,len(hor)):
            
            if(car2==car):
                continue

            And_Predicate1.append(Position_Horizontal[turn+1][car2]==Position_Horizontal[turn][car2])

        for car2 in range(0,len(ver)):
            And_Predicate1.append(Position_Vertical[turn+1][car2]==Position_Vertical[turn][car2])
        
        And_Predicate1.append(Position_Horizontal[turn+1][car]==Position_Horizontal[turn][car]+1)

        #Mine
        
        #for i in range(0,len(mines)):
        #    And_Predicate1.append(Position_Horizontal[turn+1][car]!=Mines[i])

        #Collision
        
        #for car2 in range(0,len(hor)):

        #    if(car==car2):
        #        continue
            
        #    And_Predicate1.append(Position_Horizontal[turn+1][car2]!=Position_Horizontal[turn+1][car]+1)

        #for car2 in range(0,len(ver)):

        #    And_Predicate1.append(Position_Vertical[turn+1][car2]!=Position_Horizontal[turn+1][car])
        #    And_Predicate1.append(Position_Vertical[turn+1][car2]!=Position_Horizontal[turn+1][car]+board_size)

        Or_Predicate1[1]=And(And_Predicate1)

        s.add(Or(Or_Predicate1))

        ### Backward Move

        Or_Predicate2=[None]*2

        Or_Predicate2[0] = Not(Moves[turn]==2*ind+1)

        And_Predicate2=[]

        #Boundary Condition
        
        #And_Predicate2.append((Position_Horizontal[turn][car])%board_size!=0)
        #And_Predicate2.append((Position_Horizontal[turn][car])%board_size!=1)

        #Propagation

        for car2 in range(0,len(hor)):
            
            if(car2==car):
                continue

            And_Predicate2.append(Position_Horizontal[turn+1][car2]==Position_Horizontal[turn][car2])

        for car2 in range(0,len(ver)):
            And_Predicate2.append(Position_Vertical[turn+1][car2]==Position_Vertical[turn][car2])
        
        And_Predicate2.append(Position_Horizontal[turn+1][car]==Position_Horizontal[turn][car]-1)

        #Mine
        
        #for i in range(0,len(mines)):
        #    And_Predicate2.append(Position_Horizontal[turn+1][car]-1!=Mines[i])

        #Collision
        
        #for car2 in range(0,len(hor)):

        #    if(car==car2):
        #        continue
            
        #    And_Predicate2.append(Position_Horizontal[turn+1][car2]!=Position_Horizontal[turn+1][car]-1)

        #for car2 in range(0,len(ver)):

        #    And_Predicate2.append(Position_Vertical[turn+1][car2]!=Position_Horizontal[turn+1][car]-1)
        #    And_Predicate2.append(Position_Vertical[turn+1][car2]!=Position_Horizontal[turn+1][car]+board_size-1)

        Or_Predicate2[1]=And(And_Predicate2)

        s.add(Or(Or_Predicate2))
        ind+=1

    for car in range (0,len(ver)):
        
        ### Down Move

        Or_Predicate1=[None]*2

        Or_Predicate1[0] = Not(Moves[turn]==2*ind)

        And_Predicate1=[]

        #Boundary Condition
        
        #And_Predicate1.append((Position_Vertical[turn][car])/board_size!=board_size-1)

        #Propagation

        for car2 in range(0,len(hor)):
            
            And_Predicate1.append(Position_Horizontal[turn+1][car2]==Position_Horizontal[turn][car2])

        for car2 in range(0,len(ver)):
                        
            if(car2==car):
                continue

            And_Predicate1.append(Position_Vertical[turn+1][car2]==Position_Vertical[turn][car2])
        
        And_Predicate1.append(Position_Vertical[turn+1][car]==Position_Vertical[turn][car]+board_size)

        #Mine
        
        #for i in range(0,len(mines)):
        #    And_Predicate1.append(Position_Vertical[turn+1][car]!=Mines[i])

        #Collision
        
        #for car2 in range(0,len(hor)):

        #    And_Predicate1.append(Position_Horizontal[turn+1][car2]!=Position_Vertical[turn+1][car])
        #    And_Predicate1.append(Position_Horizontal[turn+1][car2]!=Position_Vertical[turn+1][car]+1)

        #for car2 in range(0,len(ver)):
            
        #    if(car==car2):
        #        continue
            
        #    And_Predicate1.append(Position_Vertical[turn+1][car2]!=Position_Vertical[turn+1][car]+board_size)

        Or_Predicate1[1]=And(And_Predicate1)

        s.add(Or(Or_Predicate1))

        ### Up Move

        Or_Predicate2=[None]*2

        Or_Predicate2[0] = Not(Moves[turn]==2*ind+1)

        And_Predicate2=[]

        #Boundary Condition
        
        #And_Predicate2.append((Position_Vertical[turn][car])/board_size!=0)
        #And_Predicate2.append((Position_Vertical[turn][car])/board_size!=1)

        #Propagation

        for car2 in range(0,len(hor)):

            And_Predicate2.append(Position_Horizontal[turn+1][car2]==Position_Horizontal[turn][car2])

        for car2 in range(0,len(ver)):
            
            if(car2==car):
                continue
            And_Predicate2.append(Position_Vertical[turn+1][car2]==Position_Vertical[turn][car2])
        
        And_Predicate2.append(Position_Vertical[turn+1][car]==Position_Vertical[turn][car]-board_size)

        #Mine
        
        #for i in range(0,len(mines)):
        #    And_Predicate2.append(Position_Vertical[turn+1][car]!=Mines[i]+board_size)

        #Collision
        
        #for car2 in range(0,len(ver)):

        #    if(car==car2):
        #        continue
            
        #    And_Predicate2.append(Position_Vertical[turn+1][car2]!=Position_Vertical[turn+1][car]-board_size)

        #for car2 in range(0,len(hor)):

        #    And_Predicate2.append(Position_Horizontal[turn+1][car2]!=Position_Vertical[turn+1][car]-board_size)
        #    And_Predicate2.append(Position_Horizontal[turn+1][car2]!=Position_Vertical[turn+1][car]-board_size+1)

        Or_Predicate2[1]=And(And_Predicate2)

        s.add(Or(Or_Predicate2))
        ind+=1
    
    ### No Move
    Or_Predicate3=[None]*2

    Or_Predicate3[0]=Not(Moves[turn]==(2*ind))

    And_Predicate3=[]

    for car2 in range(0,len(hor)):
            
        And_Predicate3.append(Position_Horizontal[turn+1][car2]==Position_Horizontal[turn][car2])

    for car2 in range(0,len(ver)):

        And_Predicate3.append(Position_Vertical[turn+1][car2]==Position_Vertical[turn][car2])
    
    Or_Predicate3[1]=And(And_Predicate3)

    s.add(Or(Or_Predicate3))

#Boundary

#for turn in range(0,num_moves_max):
#    s.add(Or(Moves[turn]/2 >= len(hor),Moves[turn]%2==1,Position_Horizontal[turn][Moves[turn]/2]!=board_size-1))

for turn in range(1,num_moves_max):
    for car in range(0,len(hor)):
        s.add(Or(Position_Horizontal[turn][car]%board_size!=board_size-1,Moves[turn]!=2*car))

for turn in range(1,num_moves_max+1):
    for car in range(0,len(hor)):
        s.add(Position_Horizontal[turn][car]%board_size!=0)

for turn in range(1,num_moves_max):
    for car in range(0,len(ver)):
        s.add(Or(Position_Vertical[turn][car]/board_size!=board_size-1,Moves[turn]!=2*(len(hor)+car)))

for turn in range(1,num_moves_max+1):
    for car in range(0,len(ver)):
        s.add(Position_Vertical[turn][car]/board_size!=0)
#Mine

for turn in range(1,num_moves_max+1):
    for car in range(0,len(hor)):
        for co in range(0,len(mines)):
            s.add(Position_Horizontal[turn][car]!=Mines[co])
            s.add(Position_Horizontal[turn][car]-1!=Mines[co])
    for car in range(0,len(ver)):
        for co in range(0,len(mines)):
            s.add(Position_Vertical[turn][car]!=Mines[co])
            s.add(Position_Vertical[turn][car]-board_size!=Mines[co])

#Collision

for turn in range(1,num_moves_max+1):
    for car in range(0,len(hor)):
        for car2 in range(0,len(hor)):
            if car==car2:
                continue
            s.add(Or(Position_Horizontal[turn][car]%board_size==board_size-1,Position_Horizontal[turn][car]+1!=Position_Horizontal[turn][car2]))
    for car in range(0,len(ver)):
        for car2 in range(0,len(ver)):
            if car==car2:
                continue
            s.add(Or(Position_Vertical[turn][car]/board_size==board_size-1,Position_Vertical[turn][car]+board_size!=Position_Vertical[turn][car2]))
    for car in range(0,len(hor)):
        for car2 in range(0,len(ver)):
            s.add(Position_Horizontal[turn][car]!=Position_Vertical[turn][car2])
            s.add(Position_Horizontal[turn][car]-1!=Position_Vertical[turn][car2])
            s.add(Position_Vertical[turn][car2]-board_size!=Position_Horizontal[turn][car])
            s.add(Position_Vertical[turn][car2]-board_size!=Position_Horizontal[turn][car]-1)

###Final Check

s.add(Position_Horizontal[num_moves_max][0]==(hor[0][0]*board_size+board_size-1))

###### LOGIC ENDS

if s.check()==z3.sat:
    model=s.model()

    #for i in range(0,num_moves_max):
    #    print('Moves',i,model[Moves[i]])
    
    for i in range(0,num_moves_max):
        
        move = model[Moves[i]].as_long()

        if move//2<len(hor):
            if move%2==0:
                print(model[Position_Horizontal[i][move//2]].as_long()//board_size,model[Position_Horizontal[i][move//2]].as_long()%board_size,sep=',')
            if move%2==1:
                print(model[Position_Horizontal[i][move//2]].as_long()//board_size,model[Position_Horizontal[i][move//2]].as_long()%board_size-1,sep=',')
        elif move//2<len(hor)+len(ver):
            if move%2==0:
                print(model[Position_Vertical[i][move//2-len(hor)]].as_long()//board_size,model[Position_Vertical[i][move//2-len(hor)]].as_long()%board_size,sep=',')
            if move%2==1:
                print(model[Position_Vertical[i][move//2-len(hor)]].as_long()//board_size-1,model[Position_Vertical[i][move//2-len(hor)]].as_long()%board_size,sep=',')
                    
    #print(model[Position_Horizontal[0][0]],model[Position_Horizontal[1][0]])
    
    #for c in s.assertions():
    #    print(c)
    # for i in range(0,num_moves_max):
        
    #     val=0
    #     for j in range(0,len(hor)):
    #         if(model[Horizontal_Moves[i][j][0]]==True):
    #             print('Horizontal_Moves',i,j,0)
    #             val=1
    #             break
    #         if(model[Horizontal_Moves[i][j][1]]==True):
    #             print('Horizontal_Moves',i,j,1)
    #             val=1
    #             break
    #     for j in range(0,len(ver)):
    #         if(model[Vertical_Moves[i][j][0]]==True):
    #             print('Vertical_Moves',i,j,0)
    #             val=1
    #             break
    #         if(model[Vertical_Moves[i][j][1]]==True):
    #             print('Vertical_Moves',i,j,1)
    #             val=1
    #             break
    #     if val==0:
    #         print('No Move',i)

    
else:   
    print("unsat",flush=True)

#print("--- %s seconds ---" % (time.time() - start_time),flush=True)