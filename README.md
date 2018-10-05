# Creating interactive visualisations of collaboration networks with JavaScript

**For an interactive example click [here](http://www.dtc.ox.ac.uk/people/14/klimmf/networkIllustration.html)**


This script allows the creation of visualisations of your scientific collaboration network with the D3.js library. Input is a BibTex library file with all (your) publications. It works by calling the python script  *bibtex2json*, which writes a .json. The JSON is then read by html/js to create the illustration.

![Small example network](./videos/RosalindFranklinAuthorshipNetwork.gif)
![Large example network](./videos/largeExampleNetworkIllustration.mov.gif)

GitHub does not allow the presentation of JavaScript illustrations on this page, thus the figures above are just screenshots. For some interactive examples, please see my [page](http://www.dtc.ox.ac.uk/people/14/klimmf/networkIllustration.html) or download the files and check out the example, consisting of some of Rosalind Franklin's publications. A larger network, consisting of all publications of the Oxford Protein Informatics Group is shown [here](http://www.dtc.ox.ac.uk/people/14/klimmf/networkIllustrationTooltip.html). At the moment there are two variants of the illustration: one simple version with only showing the network and information as tooltips and a second with images of the authors and the papers.

Requirements:
  - python for the script running
  - python module pybtex for reading the BibTex file
  - D3, which will be loaded automatically by your browser when it is needed (using version 4)

Howto:
  - save your publications into a bibfile, e.g. MarieCurie.bib
  - edit the python file bibtex2json.py to read your input file (optional: also choose an appropriate outputfile name , e.g., MarieCurie.json)
  - run bibtex2json.py
  - look at the illustration in the html files "ForceLayoutTooltip.html" or "ForceLayoutPhoto.html"  (with Firefox, see advice below, if you changed the name of the .json you have to change it the JavaScript files that are loaded, too)

The python scripts reads some optional information from the .bib file, e.g., a url, if given by "Url" tag (see for example the franklin1951crystallite paper in the exemplary bib). If this is not given double-clicking a paper-node automatically google searches the paper title. You can also specify the image that should be shown for a certain paper by giving a link to an image file with the non-standard "image" tag (see for example the paper franklin1958structureRibo)

Furthermore you can read optional author information from a file, see `authorinfoRosalindFranklin.csv`. At the moment this is only a link to the authors homepage (opened by double clicking the node) and a link to a photo. At best you store the image locally but you can also link to an image hosted somewhere else. You don't have to give all information for all authors.

The default behaviour is that the ego node, representing the author that is on all papers, is removed. But this can be switched off, e.g., if you want to show the publications of a larger research group with multiple PIs.

Some further comments:
- If you are not happy with the steady state of the node positions, e.g., because all nodes are clumped together, you can play around with the parameters of the force layout, which are hard-coded in the java script part of the html. The current, default choices are: distanceMin(20).distanceMax(150).strength(-20)
- Warning: At the moment the script is **very** sensitive with author names. Thus, "Feynman, Richard" and "Feynman, Richard P." and "Feynman, Richard P" are all considered to be different authors.
- In general the python code is not optimised for performance but rather for readability, such that people can alter the code to fit it their custom purposes. Frankly, this seemed reasonable because the number of publications is usually not that big.
- Usually, the bib library will have special characters in a LaTeX format, e. g., {\"u} for the German umlaut ü. I wrote the small function 'latex2unicode' to replace them with unicode but you will have to adopt this to your own needs. (Let me know if there is a function that does everything automatically)

**Advice**: When you are creating the visualisations locally some browsers (Chrome and Safari) do not allow the loading of the external d3 library or your .json file. When you see only the headings but no illustration this is likely the case. Either, use Firefox (recommended for simplicity), create a local server, or debug all the code online. When you upload the .html everything works fine with the other browsers, too.

If there are problems, please open an issue on the GitHub page.
