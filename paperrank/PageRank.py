import operator
import numpy as np
import re, csv, networkx as nx
import time
import json

def parse(filename):
    reader = csv.reader(open(filename, 'r'), delimiter=',')
    data = [row for row in reader]
    return parse_directed(data)



def parse_directed(data):
    DG = nx.DiGraph()

    for i, row in enumerate(data):
        node_a = format_key(row[0])
        node_b = format_key(row[2])
        val_a = digits(row[1])
        val_b = digits(row[3])
        if val_a >= val_b:
            DG.add_edge(node_b, node_a)
        else:
            DG.add_edge(node_a, node_b)
    return DG

def digits(val):
    return int(re.sub("\D", "", val))

def format_key(key):
    key = key.strip()
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return key

class PageRank:
    def __init__(self, graph):
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85
        self.ranks = dict()

    
    def rank(self):
        for key, node in self.graph.nodes(data=True):
            self.ranks[key] = 0.0

        #power method
        A = np.zeros((len(self.graph.nodes(data=True)), len(self.graph.nodes(data=True))))
        graph_list0 = list(self.graph.nodes(data=True))
        graph_list = []
        for i in range(len(graph_list0)):
            graph_list.append(graph_list0[i][0])

        for key, node in self.graph.nodes(data=True):
            neighbors = self.graph.out_edges(key)
            for n in neighbors:
                A[graph_list.index(key), graph_list.index(n[1])] = 1
        for i in range(len(graph_list)):
            if sum(A[i,:])>0:
                A[i, :] /= sum(A[i,:])
            else:
                A[i, :] = 1 / len(graph_list)
        A *=  self.d
        A += (1-self.d) / len(graph_list)
        x0 = np.zeros(len(graph_list))
        x0[0] = 1
        for _ in range(200):
            x0 = np.dot(x0, A)
        for i in range(len(graph_list)):
            self.ranks[graph_list[i]] = x0[i]




if __name__ == '__main__':
    time_start = time.time()
    filename = "./pagerank/data/citations.csv"

    graph = parse(filename)
    p = PageRank(graph)
    p.rank()

    sorted_r = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)
    
    id_list=[]
    pagerank_dic={}
    
    for tup in sorted_r:
        id_list.append(tup[0])
        pagerank_dic[tup[0]]=tup[1]
    
    file=open('./data/local/filtered_papers.json', 'r', encoding='UTF-8')
    nopagerank=0
    with open('./data/pagerank_result.json', 'w', encoding='UTF-8') as f:
        for line in file:
            paper = json.loads(line)
            if paper['id'] not in id_list:
                nopagerank+=1
                paper['pagerank']=0
            else:
                paper['pagerank']=pagerank_dic[paper['id']]        
            f.writelines(json.dumps(paper)+'\n')
    
    file.close()
    f.close()
    time_end = time.time()
    print("total time {} s".format(time_end-time_start))


