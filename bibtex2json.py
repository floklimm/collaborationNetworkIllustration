# -*- coding: utf-8 -*-
"""
script for transfering a BibTex library (.bib-file) into a bipartite graph 
that is save into a JavaScript Object Notation file (.json), which can be read 
by JavaScript to create an interactive visualisation.

By Florian Klimm, March 2018
"""


# some options
deleteEgoNode = True
inputBibFileName = 'einstein.bib'
outputJSONFileName = 'einstein.json'

# import necessary libraries
from pybtex.database.input import bibtex # for reading the bib files
import json # for writing the json

# some preperation to read the bibtex file
parser = bibtex.Parser()
bib_data = parser.parse_file(inputBibFileName)


listOfAuthors=[] # empty list of authors

# go throuh all entries
for paperKeys in bib_data.entries.keys():
    # get the authors of this paper
    authors = bib_data.entries[paperKeys].fields['author'].split(" and ")
    # save them to the list of authors
    for author in authors:
        listOfAuthors.append(author)

# deleting ego 
if deleteEgoNode == True:
    # we assume that the author with the most entries is the ego node and delete it
     egoNode = max(listOfAuthors, key=listOfAuthors.count) # returns the ego node
     listOfAuthors = list(set(listOfAuthors)) # gets unique list of authors
     listOfAuthors.pop(listOfAuthors.index(egoNode)) # deletes it from the list of authors
else:
    listOfAuthors = list(set(listOfAuthors)) # gets unique list of authors

nAuthors = len(listOfAuthors) # number of author nodes
nPapers = len(bib_data.entries.keys()) # number of paper nodes

# create a dictionary reflecting the graph (there are more pyhtonic ways
# possible to creat this, e.g., with zip, but this is easiest)

node_list = []
# create author nodes
for i in range(nAuthors):
    node_dict = {} # create an empty dictionary for this node
    node_dict["id"] = "A" + str(i)
    node_dict["group"] = 0
    node_dict["name"] = listOfAuthors[i]
    node_list.append(node_dict)

## create paper nodes
#for i in range(nPapers):
#    node_dict = {} # create an empty dictionary for this node
#    node_dict["id"] = "P" + str(i)
#    node_dict["group"] = 2
#    node_list.append(node_dict)

# create the links between the nodes
link_list = []
i=0
for paperKeys in bib_data.entries.keys(): # go over every paper
    # create the paper node
    node_dict = {} # create an empty dictionary for this node
    node_dict["id"] = "P" + str(i)
    node_dict["group"] = 1
    node_dict["name"] =  bib_data.entries[paperKeys].fields['title']
    node_list.append(node_dict)

    # find the authors for this paper
    authorsThisPaper = bib_data.entries[paperKeys].fields['author'].split(" and ")
    
    
    
    for authors in authorsThisPaper: 
        link_dict = {} # empty dictionary for this edge
        link_dict["source"] = "P" + str(i) # attached to this paper
        try:
            link_dict["target"] = "A" + str(listOfAuthors.index(authors)) # and attached to co-author
            link_list.append(link_dict)    # save it into the list
        except ValueError:
            print("Author %s not in list, probably the ego node." %authors )
    i=i+1
    
# write into dictionary
graph_dict = {"nodes" : node_list, "links" : link_list}


 
# opening the file to write
if outputJSONFileName:
    # Writing JSON data
    with open(outputJSONFileName, 'w') as f:
        json.dump(graph_dict, f)
        
        