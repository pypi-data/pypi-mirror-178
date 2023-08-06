import pandas as pd
import math
# !pip install networkx[default]
# !pip install matplotlib==3.1.3
import networkx as nx
import numpy as np
np.random.seed(1000)
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def init_graph_attr1(G,crop,statesList,taluk_attri_Dict,states): 
  nodeAttr = {}
  init_graph1(G,states,crop,statesList)
  for i in range(len(states)):
      temp = {}
      temp['OldDeltaVector'] = np.zeros(2)
      temp["DeltaVectornodesStress"] = 0 
      temp['NewDeltaVector'] = np.zeros(2)
      temp["sdgvec"] = taluk_attri_Dict[statesList[i]]
      temp["tempsdgvec"] = taluk_attri_Dict[statesList[i]]
      temp["oldsdgvec"] = taluk_attri_Dict[statesList[i]]
      temp["nodesStress"] = 0
      temp["meansdg"] = np.mean(taluk_attri_Dict[statesList[i]])
      temp["name"] = statesList[i]
      # temp["Tempsdgvec"] = stateSDGDict[i] 
      nodeAttr[i] = temp
  print(nodeAttr)
  nx.set_node_attributes(G, nodeAttr)

def init_graph1(G,states,crop,statesList): #states is a dataframe
    G.add_nodes_from([i for i in range(0,len(states))])
    # print(len(states))
    labels = {}
    labels = states.columns
    print(labels[0])
    for i in range(len(states)):
      #  labels[i] = statesList[i]
      #  print(states.columns[1][i])
      #  print( states[labels[0]][i])
       snode=  states[labels[0]][i]-1
       temp = states[labels[2]][i]
      #  print(temp)
      #  temp=states[str(states.columns[2])][i]
       #print(temp)
       if ',' in str(temp):
          sedge_arr=temp.split(',')
          #print(sedge_arr)
          for i in range(0,len(sedge_arr)):
              G.add_edge(snode,int(sedge_arr[i])-1)
              
       elif math.isnan(temp) :
          print()
       else :
          G.add_edge(snode,temp-1)
          # print(snode,temp-1)
    # my_pos = nx.spring_layout(G, seed = 1000)
    # node_sizes = df[crop]*3000
    # print(statesList)
    # H1=nx.draw(G,pos=my_pos,with_labels=True, labels=labels,node_size=node_sizes,node_color=df[crop].astype(float)*300, cmap=plt.cm.Blues)
    return 

def getMeanSDGGraph2(G,label,num):
  meanSDG = 0
  for n in G.nodes():
    meanSDG += np.mean(np.array(G.nodes[n][label]))
  #print(meanSDG," ",num)
  return meanSDG / num

def getGraphStress2(G,label):
  for n in G.nodes():
    nodeStress = 0
    neigList = list(G.neighbors(n))
    for nei in neigList:
      a = np.array(G.nodes[n][label])
      b = np.array(G.nodes[nei][label])
      nodeStress += np.linalg.norm((a - b), ord=1)
    G.nodes[n]["nodesStress"] = nodeStress
    
  stress = 0
  for n in G.nodes():
    stress += G.nodes[n]["nodesStress"]
  return stress

def StressReduction(G, label1,label2,numSDG):
  for n in G.nodes():
      nodeStress = 0
      neigList = list(G.neighbors(n))
      a = np.zeros(numSDG)
      for nei in neigList:
        a = np. add(a,np.array(G.nodes[nei][label1]))
      if len(neigList)!=0:
        a = a/len(neigList)
        G.nodes[n][label2] = np.add(G.nodes[n][label2],np.add(a,-1*np.array(G.nodes[n][label1]))).tolist()
  for n in G.nodes():
    G.nodes[n][label1] = G.nodes[n][label2].copy()
  return 


def graphCalliberation(numRounds,EpsilonStress,crop,statesList,numSDG,final,attribute_list,taluk_attri_Dict,states):
  statesDict = {}
  for i in statesList:
    statesDict[i] = []
  G3= nx.Graph()
  MeanSDGs = []
  MeanStress = [] 
  XAxis = []
  init_graph_attr1(G3,crop,statesList,taluk_attri_Dict,states)
  # print("Punjabs SDG 5 after Policy Intervention:",G2.nodes[19]['sdgvec'])
  # PolicyIntervention(G,label,nodeIDs,Policies)
  for i in range(numRounds):
    temp1 = getMeanSDGGraph2(G3,"sdgvec",len(attribute_list))
    temp2 = getGraphStress2(G3,"sdgvec")
    XAxis.append(i)
    #print(" Mean SDG Graph is: ",temp1," Graph Stress is:",temp2)
    MeanSDGs.append(temp1)
    MeanStress.append(temp2)
    for n in G3.nodes(): 
      print(G3.nodes[n]["name"])
      statesDict[G3.nodes[n]["name"]].append(G3.nodes[n]["sdgvec"])
    if temp2>=EpsilonStress:
      # PolicyIntervention(G,Policies,NodeIDs,numSDGs,label)
      StressReduction(G3,"sdgvec" ,"tempsdgvec",numSDG)
    else:
      break
  print("Till her it cames\n")
  for n in G3.nodes(): 
    statesDict[G3.nodes[n]["name"]].append(G3.nodes[n]["sdgvec"])
  print("Till here also it cames\n")
  return statesDict


def StressModelling(numNodes,numSDG,numOfRounds,BeforeATEFile,AfterATEFile,adjList):
    # Importing neccessary libraries
 

    # numNodes = 10  # Input 
    # numSDG = 2  #Input
    # numOfRounds = 3 #Input 
    myseed = 1000
    epsilonStress = 0.5
    maxRounds = 1000 
    numPolicies = 100
    # BeforeATEFile = "/content/sample_data/ATEAfter.xlsx" #Input 
    # AfterATEFile = '/content/sample_data/ATEBefore.xlsx' #Input 
    # adjList = '/content/sample_data/Adjacent list ac zones.xlsx' #Input 
    df = pd.read_excel(BeforeATEFile)
    df2=pd.read_excel(AfterATEFile)
    attribute_list= list(df.columns[2:])
    labels = list(df[df.columns[1]])
    print(attribute_list)
    print(labels)

    df['sdgvec'] = df[attribute_list].values.tolist()
    taluk_attri_Dict = dict(zip(df[df.columns[1]], df.sdgvec))
    df2['sdgvec'] = df2[attribute_list].values.tolist()
    states=pd.read_excel(adjList)
    statesList = list(states[states.columns[1]])
    print("States is: ")
    print(states)
    # G1 = nx.Graph()
    # init_graph_attr1(G1,attribute_list[0])
    final = {}
    return graphCalliberation(numOfRounds,epsilonStress,attribute_list[0],statesList,numSDG,final,attribute_list,taluk_attri_Dict,states)

# Results = StressModelling(10,2,3,r"./ATEBefore.xlsx",r"./ATEAfter.xlsx",r"./Adjacent list ac zones.xlsx")
# def print_obj(Results):
#   for i in Results.keys():
#     print(Results[i])
# print_obj(Results)

# [1, 0.6072341817382682, 0.27183721596378846]
# [2, 0.6052543238455066, 0.47738041800580117]
# [3, 0.6410805675368592, 0.48453300733656623]
# [4, 0.6065932080056674, 0.38434592963797076]
# [5, 0.6100092966386761, 0.33331147865550675]
# [6, 0.6084824906414215, 0.31281713769793634]
# [7, 0.6034939935041791, 0.3100125548854487]
# [8, 0.6083756577938256, 0.3121952851981454]
# [9, 0.6101261019554216, 0.32884948600885133]
# [10, 0.6084663183549093, 0.3272474482163977]