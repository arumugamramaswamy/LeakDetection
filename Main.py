from math import log,factorial
import itertools
import networkx as nx
from networkx.algorithms.community import kernighan_lin_bisection
import numpy as np
from operator import itemgetter
from Front_end import front_end

labels = []

class watersystem:

    def __init__(self,graphmatrix,inflow_list=None):

        #storing the graph 
        self.graph = graphmatrix
        self.nodes = [0 for x in range(len(graphmatrix))]
        self.edgeflow = []
        #creating a node object for all nodes
        for x in range(len(graphmatrix)):
            self.nodes[x] = node(str(x))

        #when inflow list is inputted
        if inflow_list != None:

            #sorting the inflow list based on node numbers
            inflow_list = sorted(inflow_list, key=itemgetter(0)) 
            
            #creating a list of inflow nodes
            self.inflow_nodes = [inflow_list[x][0] for x in range(len(inflow_list))]

            #modifying inflow values for the nodes
            for x in range(len(inflow_list)):
                self.nodes[x].inflow_modify(inflow_list[x][1])
        else:
            self.inflow_nodes = None


    def get_outflows(self):
        if self.inflow_nodes != None:
            #iterating through present nodes
            for x in self.nodes:
                keep_going = True
                if int(x.name) not in self.inflow_nodes:
                    while keep_going:
                        keep_going = False
                        try:
                            outflow = int(input("enter the outflow value for node "+str(int(x.name)+1)+" (inflow is -ve)"))
                            x.outflow_modify(outflow)
                        except:
                            keep_going = True
        else:
            for x in self.nodes:
                keep_going = True
                while keep_going:
                    keep_going = False
                    try:
                        outflow = int(input("enter the outflow value for node "+str(int(x.name)+1)+" (inflow is -ve)"))
                        x.outflow_modify(outflow)
                    except:
                        keep_going = True
    
    def get_edgeflow(self,edge):
        keep_going = True
        while keep_going:
            keep_going = False
            try:
                edge_flow = int(input("enter the flow between nodes "+str(edge[0]+1)+" and "+str(edge[1]+1)+" (direction matters, if flow is opposite use a -ve sign)"))
                self.edgeflow.append((edge,edge_flow))
            except:
                keep_going = True
        return edge_flow
        



class node:

    def __init__ (self,Name):
        self.inflow = None
        self.outflow = None
        self.name = Name

    def inflow_modify(self,value_inflow):
        self.inflow = value_inflow

    def outflow_modify(self,value_outflow):
        self.outflow = value_outflow



def delduplicates(anylist):
    for x in range(len(anylist)):
        for y in range(x + 1, len(anylist)):
            if anylist[x] == anylist[y]:
                anylist[y] = '_'
        while '_' in anylist:
            anylist.remove('_')


#returns all the nodes which can be reached from 0th node
def path_zero(graphmatrix):
    # the nth element of mega list states what nodes the nth node is connected to
    megalist = []
    for i in range(len(graphmatrix)):
        smalllist = []
        for j in range(len(graphmatrix)):
            if graphmatrix[i][j] == 1:
                smalllist.append(j)
        megalist.append(smalllist)

    beforedel = []
    # zero connection = what and all 0 is connected to
    zeroconnection = megalist[0]
    x = 0
    while len(beforedel) != len(zeroconnection):
        x += 1
        for i in zeroconnection:

            zeroconnection += megalist[i]

            if x > 1:
                beforedel = zeroconnection

            delduplicates(zeroconnection)

    return zeroconnection

#calls path_zero and returns adjacency list
def adjacency_return(graphmatrix):
    counter = 0
    adjacency_list = [0 for x in graphmatrix]
    zeroconnection = path_zero(graphmatrix)
    for x in range(len(adjacency_list)):
        if zeroconnection.count(x) == 1:
            adjacency_list[x] = 1
    # adjacency list's nth element will be 1 if the nth node can be reached from the 0th node
    return adjacency_list

#calls adjacency return and states whether disjoint or connected
def if_disjoint(graphmatrix):
    adjacency_list =adjacency_return(graphmatrix)
    if 0 in adjacency_list:
        print("disjoint")
        return True
    else:
        print("connected")
        return False

def subgraph(disjgraph):
    # in the adjacency list postion of all zeros is put in zero list
    zerolist=[]
    # in the adjacency list postion of all ones is put in one list
    onelist=[]
    adjacencylist = adjacency_return(disjgraph)
    for x in range(len(adjacencylist)):
        if adjacencylist[x]==0:
            zerolist.append(x)
        else:
            onelist.append(x)

    #creates a new graph matrix for onelist
    onemat = [[0 for x in range(len(onelist))] for x in range(len(onelist))]
    
    #creates a new graph matrix for zerolist
    zeromat = [[0 for x in range(len(zerolist))] for x in range(len(zerolist))]
    
    for x in range(len(onelist)):
        for y in range(len(onelist)):
            onemat[x][y] = disjgraph[onelist[x]][onelist[y]]                 
    
    for x in range(len(zerolist)):
            for y in range(len(zerolist)):
                zeromat[x][y]=disjgraph[zerolist[x]][zerolist[y]]
    
    subgraph={   
                "zeromat":zeromat,
                "onemat":onemat,
                "zerolist":zerolist,
                "onelist":onelist
                }
    
    return subgraph

#first converts the graphmatrix into a networkx graph object then carries out kernighan lin bisection
#this divides the graph into two sets of nodes
def networkx_manipulator(graphmatrix):

    #new graph object
    G = nx.Graph()
    
    #adding nodes
    G.add_nodes_from([x for x in range(len(graphmatrix))])

    #adding edges
    for x in range(len(graphmatrix)):
        for y in range(len(graphmatrix)):
            if graphmatrix[x][y]==1:
                G.add_edge(x,y)

    return kernighan_lin_bisection(G)


#from the kernighan lin bisection we generate the cutset
def cut_generator(graphmatrix):

    subgraphs = networkx_manipulator(graphmatrix)
    
    #storing nodes of the two subgraphs created using kernighan lin bisection
    sub1 = list(subgraphs[0])
    sub2 = list(subgraphs[1])

    #creating a new graphmatrix based on the original graphmatrix 
    #and not copying the edges between the two seperate partions created by kernighan lin bisection
    graphmatrix_new = [[0 for x in range(len(graphmatrix))] for x in range(len(graphmatrix))]

    for x in sub1:
        for y in sub1:
            if graphmatrix[x][y]==1:
                graphmatrix_new[x][y] = 1

    for x in sub2:
        for y in sub2:
            if graphmatrix[x][y]==1:
                graphmatrix_new[x][y] = 1

    #subtracting the two graphs to get which edges we have to remove
    graphmatrixnp = np.array(graphmatrix)
    graphmatrix_newnp = np.array(graphmatrix_new)
    res_graph = graphmatrixnp - graphmatrix_newnp

    #storing the edges to be removed in cut
    cut =[]
    for x in range(len(graphmatrix)):
        for y in range(x):
            if res_graph[x][y]==1:
                cut.append((x,y))

    return cut

def del_from_graph(graphmatrix,n,water_system,count = 1):

    # first call of the recursive function
    if count==0:
        count =1
        temp=[]
        n = len(graphmatrix)
        for x in range(n):
            temp.append(x)
        labels.append(temp)

    #check which cuts to make
    new_graphmatrix =graphmatrix
    print(np.array(new_graphmatrix))
    cuts= cut_generator(graphmatrix)
    print(cuts)

    #begin making cuts
    for x in cuts:
        new_graphmatrix[x[0]][x[1]]= 0
        new_graphmatrix[x[1]][x[0]]= 0
    
    #get edgeflow for cuts
    for cut in cuts:
        real_cut = (labels[-1].index(cut[0]),labels[-1].index(cut[1]))
        edge_flow = water_system.get_edgeflow(real_cut)
        water_system.nodes[real_cut[0]].outflow_modify(water_system.nodes[real_cut[0]].outflow+edge_flow)
        water_system.nodes[real_cut[1]].outflow_modify(water_system.nodes[real_cut[1]].outflow-edge_flow)

    #check whether graph has been completely segmented
    one_D_graphmatrix = []
    for x in range(len(graphmatrix)):
        one_D_graphmatrix+=graphmatrix[x]        
    
    if 1 in one_D_graphmatrix:
        graphmatrixdict = subgraph(new_graphmatrix)
        tot=0
        for x in range(len(graphmatrixdict["onelist"])):
            node_cur = graphmatrixdict["onelist"][x]
            real_node = labels[-1].index(node_cur)
            tot += water_system.nodes[real_node].outflow

        if tot != 0: #add direction here
            graphmatrix = graphmatrixdict["onemat"]
            temp=["x" for x in range(n)]
            cnt = 0
            for x in labels[len(labels)-1]:
                for y in graphmatrixdict["onelist"]:
                    if x == y:
                        temp[cnt]=(graphmatrixdict["onelist"].index(y))
                        break
                cnt+=1
            labels.append(temp)
            del_from_graph(graphmatrix,n,water_system)
        else:
            graphmatrix = graphmatrixdict["zeromat"]
            cnt =0
            for x in labels[len(labels)-1]:
                temp[x]="x"
                for y in graphmatrixdict["zerolist"]:
                    if x == y:
                        temp[cnt]=(graphmatrixdict["zerolist"].index(y))
                        break
                cnt+=1
            labels.append(temp)
            del_from_graph(graphmatrix,n,water_system)
    else:
        print("all done")
        print(labels)
            


# test

gra_con =[[0,1,0,1,0],
        [1,0,0,0,1],
        [0,0,0,1,1],
        [1,0,1,0,0],
        [0,1,1,0,0],]

gra = [[0,1,0,0,0],
        [1,0,0,0,0],
        [0,0,0,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],]
gmat = [[0, 0, 0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1, 0, 0],       [0, 0, 1, 0, 0, 0, 0, 1, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1],       [1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0]]

new_test_1 = [[0,1,0,1,0,0,0,0],
[1,0,1,0,0,0,0,0],
[0,1,0,1,1,0,0,0],
[1,0,1,0,0,0,0,0],
[0,0,1,0,0,1,0,1],
[0,0,0,0,1,0,1,0],
[0,0,0,0,0,1,0,1],
[0,0,0,0,1,0,1,0],
]

new_test_2 = [[0,1,1,0,0,0,1],
[1,0,1,1,0,0,0],
[1,1,0,0,1,1,0],
[0,1,0,0,1,0,0],
[0,0,1,1,0,1,0],
[0,0,1,0,1,0,1],
[1,0,0,0,0,1,0]]

new_test_3 = [[0,0,1,0,0,0,0,1],
[0,0,0,1,0,0,0,1],
[1,0,0,1,0,0,1,0],
[0,1,1,0,1,1,0,0],
[0,0,0,1,0,1,1,0],
[0,0,0,1,1,0,1,1],
[0,0,1,0,1,1,0,1],
[1,1,0,0,0,1,1,0],
]


#del_from_graph(new_test_2,len(new_test_2),count = 0)
#inflow = [(0,1)]
mat = front_end()
water = watersystem(mat)
water.get_outflows()
del_from_graph(water.graph,len(water.graph),water,count =0)
#water = watersystem(new_test_1)
#water.get_edgeflow((0,1))
#water.get_outflows()

