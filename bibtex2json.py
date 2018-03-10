# -*- coding: utf-8 -*-
"""
script for transfering a BibTex library (.bib-file) into a bipartite graph 
that is save into a JavaScript Object Notation file (.json), which can be read 
by JavaScript to create an interactive visualisation.

By Florian Klimm, March 2018
"""


## some options
inputBibFileName = 'publications_Florian_Klimm.bib'
outputJSONFileName = 'fklimm.json'
#
authorInformationFile = 'authorInfoKlimm.csv' # optional co-author information
deleteEgoNode = True
##

# import necessary libraries
from pybtex.database.input import bibtex # for reading the bib files
import json # for writing the json
import csv # for loading comma seperated values
import re


# some auxiliary functions   
# you migth have to add further repalcement rules      
def latex2HTML( latexString ):
    "takes the name of an author as string and return the string with latex character replaced as normal string for the HTML"
    latexString = latexString.replace('{\\"u}' ,'ü')
    latexString = latexString.replace('{\\\'o}' ,'ó')
    latexString = latexString.replace('{\\\'a}' ,'á')
    return(latexString)
        


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
     print("Removing the ego node: %s " %egoNode )
else:
    listOfAuthors = list(set(listOfAuthors)) # gets unique list of authors

nAuthors = len(listOfAuthors) # number of author nodes
nPapers = len(bib_data.entries.keys()) # number of paper nodes


# read the additional author information from the csv
authorLinks_dict = {} # create an empty dictionary
authorImage_dict = {} # create an empty dictionary
try:
    authorInfo_reader = csv.DictReader(open(authorInformationFile))
    for row in authorInfo_reader:
        authorLinks_dict[row['name']] = row['url']
        authorImage_dict[row['name']] = row['image']
except FileNotFoundError:
    print("no optional co-author information available")






# create a dictionary reflecting the graph (there are more pythonic ways
# possible to creat this, e.g., with zip, but this is easiest)
node_list = []
# create author nodes
for i in range(nAuthors):
    node_dict = {} # create an empty dictionary for this node
    node_dict["id"] = "A" + str(i)
    node_dict["group"] = 0
    # invert the name such that the given name is before the last name
    authorSplit = listOfAuthors[i].split(",")
    nameThisAuthor = authorSplit[1][1::] + ' ' + authorSplit[0]
    
    nameThisAuthorHTML = latex2HTML(nameThisAuthor)
    print(nameThisAuthorHTML)
    node_dict["name"] = nameThisAuthorHTML
    node_list.append(node_dict)
    # try to set the url for this author
    try:
        node_dict["url"] = authorLinks_dict[nameThisAuthor]
    except KeyError:
        node_dict["url"] = "https://www.google.com/search?q=" + nameThisAuthor
        
        # try to set a image for this author
    try:
        node_dict["image"] = authorImage_dict[nameThisAuthor]
    except KeyError: # if no image jsut leave blank
        node_dict["image"] = []
        
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
    thisPaperName = bib_data.entries[paperKeys].fields['title']
    # remove curly bracket in paper name, remove it
    if thisPaperName[0]=='{':
        thisPaperName=thisPaperName[1:-1]
    node_dict["name"] =  thisPaperName
    node_list.append(node_dict)

    # find the authors for this paper
    authorsThisPaper = bib_data.entries[paperKeys].fields['author'].split(" and ")
    
    # if the paper has a url, add it
    try:
        node_dict["url"] = bib_data.entries[paperKeys].fields['url']
    except KeyError: # otherwise refer to google
        node_dict["url"] = "https://www.google.com/search?q=" + bib_data.entries[paperKeys].fields['title']
    
    
    for authors in authorsThisPaper: 
        link_dict = {} # empty dictionary for this edge
        link_dict["source"] = "P" + str(i) # attached to this paper
        try:
            link_dict["target"] = "A" + str(listOfAuthors.index(authors)) # and attached to co-author
            link_list.append(link_dict)    # save it into the list
        except ValueError:
            pass
            #print("Author %s not in list, probably the ego node." %authors )
    i=i+1
    
# write into dictionary
graph_dict = {"nodes" : node_list, "links" : link_list}


# opening the file to write
if outputJSONFileName:
    # Writing JSON data
    with open(outputJSONFileName, 'w') as f:
        json.dump(graph_dict, f)
        
