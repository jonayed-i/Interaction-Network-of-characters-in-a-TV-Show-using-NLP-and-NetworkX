import argparse
import os,sys
import os.path as osp
import json
import pandas as pd
import re
import string
import networkx as nx

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-i", type=str, nargs='?', const='arg_was_not_given')
    parser.add_argument("--output", "-o", type=str, nargs='?', const='arg_was_not_given')

    args = parser.parse_args()
    datafile = args.data
    outputpath = args.output

    with open(datafile, "r") as file:
        data = json.load(file)

    G = nx.Graph()

    for key in data:
        myfriends = data[key]
        for homie in myfriends:

            G.add_edge(key,homie,weight =data[key][homie])

    #py(G.size())
    #print(len(G))


    topbynumberofedges = list(nx.degree_centrality(G).keys())[:3]
    #print(topbynumberofedges)
    weightedcentrality = dict(G.degree(weight='weight'))
    #print(dict(weightedcentrality))
    sortweights = {k: v for k, v in sorted(weightedcentrality.items(),reverse= True, key=lambda item: item[1])}
    sortedweightslist = list(sortweights.keys())[:3]

    between = nx.betweenness_centrality(G)
    sortbetween = {k: v for k, v in sorted(between.items(), reverse=True, key=lambda item: item[1])}
    betweenlist = list(sortbetween.keys())[:3]

    outputdic = {
        "most_connected_by_num": topbynumberofedges,
        "most_connected_by_weight":sortedweightslist,
        "most_central_by_betweenness":betweenlist
    }
    with open(outputpath, 'w') as output:
        json.dump(outputdic, output, indent=2)
if __name__ == '__main__':
        main()