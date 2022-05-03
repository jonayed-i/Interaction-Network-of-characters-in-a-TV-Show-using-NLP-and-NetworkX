import argparse
import os,sys
import os.path as osp
import json
import pandas as pd
import re
import string



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-i", type=str, nargs='?', const='arg_was_not_given')
    parser.add_argument("--output", "-o", type=str, nargs='?', const='arg_was_not_given')

    args = parser.parse_args()
    datafile = args.data
    outputpath = args.output

    df = pd.read_csv(datafile,header=0)


    current = None
    ponies = {}
    interactions = {}
    currentepisode = None
    badwords = ["others","ponies","and","all"]
    for index,row in df.iterrows():


        if any( bad in row['pony'].lower() for bad in badwords):
            current = None
        elif currentepisode != row['title']:
            current = None
            currentepisode = row['title']
        else:

            currentpony = row['pony'].lower()
            if current == None:
                current = currentpony
                if currentpony not in ponies:
                    ponies[currentpony] = 1
                else:
                    ponies[currentpony] += 1

            elif current == currentpony:
                ponies[currentpony] += 1

            else:
                if currentpony not in ponies:
                    ponies[currentpony] = 1
                else:
                    ponies[currentpony] += 1

                if currentpony not in interactions:
                    interactions[currentpony] = {}
                if current not in interactions:
                        interactions[current] = {}





                if current in interactions[currentpony]:
                    interactions[currentpony][current] += 1
                    interactions[current][currentpony] += 1

                else:
                    interactions[currentpony][current] = 1
                    interactions[current][currentpony] = 1
                #print(current)
                #print(currentpony)
                current = currentpony

    goodpony = sorted(ponies, key=ponies.get, reverse=True)[:101]
    interactionslist = list(interactions.keys())
    for p in interactionslist:
        if p not in goodpony:
            del (interactions[p])

    for key in interactions:
        currentdic = interactions[key]
        interactionslist = list(currentdic.keys())
        for p in interactionslist:
            if p not in goodpony:
                del (interactions[key][p])


    #for k, v in list(interactions.items()):

    with open(outputpath, 'w') as output:
        json.dump(interactions, output,indent=2)




if __name__ == '__main__':
        main()