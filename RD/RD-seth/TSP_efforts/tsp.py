"""
tsp.py:  solve the traveling salesman problem 

minimize the travel cost for visiting n customers exactly once
approach:
    - start with assignment model
    - add cuts until there are no sub-cycles

Copyright (c) by Joao Pedro PEDROSO and Mikio KUBO, 2012
"""
import math
import time
import random
import networkx
from gurobipy import *

def solve_tsp(V,c):
    """solve_tsp -- solve the traveling salesman problem 
       - start with assignment model
       - add cuts until there are no sub-cycles
    Parameters:
        - V: set/list of nodes in the graph
        - c[i,j]: cost for traversing edge (i,j)
    Returns the optimum objective value and the list of edges used.
    """
    
    def addcut(cut_edges):
        G = networkx.Graph()
        G.add_edges_from(cut_edges)
        Components = networkx.connected_components(G)

        if len(Components) == 1:
            return False
        for S in Components:
            model.addConstr(quicksum(x[i,j] for i in S for j in S if j>i) <= len(S)-1)
            print "cut: len(%s) <= %s" % (S,len(S)-1)
        return True


    def addcut2(cut_edges):
        G = networkx.Graph()
        G.add_edges_from(cut_edges)
        Components = networkx.connected_components(G)

        if len(Components) == 1:
            return False
        for S in Components:
            T = set(V) - set(S)
            print "S:",S
            print "T:",T
            model.addConstr(quicksum(x[i,j] for i in S for j in T if j>i) >= 2)
            print "cut: %s <--> %s >= 2" % (S,T), [(i,j) for i in S for j in T if j>i]
        return True


    # main part of the solution process:
    model = Model("tsp")

    # model.Params.OutputFlag = 0 # silent/verbose mode
    x = {}
    for i in V:
        for j in V:
            if j > i:
                x[i,j] = model.addVar(ub=1, name="x(%s,%s)"%(i,j))
    model.update()
    
    for i in V:
        model.addConstr(quicksum(x[j,i] for j in V if j < i) + \
                        quicksum(x[i,j] for j in V if j > i) == 2, "Degree(%s)"%i)

    model.setObjective(quicksum(c[i,j]*x[i,j] for i in V for j in V if j > i), GRB.MINIMIZE)

    EPS = 1.e-6
    while True:
        model.optimize()
        edges = []
        for (i,j) in x:
            if x[i,j].X > EPS:
                edges.append( (i,j) )

        if addcut(edges) == False:
            if model.IsMIP:     # integer variables, components connected: solution found
                break
            for (i,j) in x:     # all components connected, switch to integer model
                x[i,j].VType = "B"
            model.update()

    return model.ObjVal,edges


def distance(x1,y1,x2,y2):
    """distance: euclidean distance between (x1,y1) and (x2,y2)"""
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def make_data(n):
    """make_data: compute matrix distance based on euclidean distance"""
    V = range(1,n+1)
    x = dict([(i,random.random()) for i in V])
    y = dict([(i,random.random()) for i in V])
    c = {}
    for i in V:
        for j in V:
            if j > i:
                c[i,j] = distance(x[i],y[i],x[j],y[j])
    return V,c
    
            
if __name__ == "__main__":
    import sys

    # Parse argument
    if len(sys.argv) < 2:
        print "Usage: %s instance" % sys.argv[0]
        exit(1)
        # n = 200
        # seed = 1
        # random.seed(seed)
        # V,c = make_data(n)

    from read_tsplib import read_tsplib
    try:
        V,c,x,y = read_tsplib(sys.argv[1])
    except:
        print "Cannot read TSPLIB file",sys.argv[1]
        exit(1)
    
    V=9

    obj,edges = solve_tsp(V,c)

    print
    print "Optimal tour:",edges
    print "Optimal cost:",obj
    print