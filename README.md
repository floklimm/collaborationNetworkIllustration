# collaboration_network
Creating interactive visualisations of collaboration networks with JavaScript

This allows the creation of visulisations of your scientific collaboration network with the D3.js library. Input is a BibTex library file with all (your) publications. It works by calling the python script  *bibtex2json*, which writes a .json. The JSON is then read by html/js to create the illustration.

Requirements:
  - python for the script running
  - python module pybtex for reading the BibTex file
  - D3, which will be loaded automatically by your browser when it is needed

Howto:
  - save your publications into a bibfile, e.g. MarieCurie.bib
  - edit the python file bibtex2json.py to read your input file (optional: also choose an appropriate outputfile name , e.g., MarieCurie.json)
  - run bibtex2json.py
  - look at the illustration (with Firefox, see advice below, if you changed the name of the .json you also have to change it here)

If you are not happy with the steady state of the node positions, e.g., because all nodes are clumped together, you can play around with the parameters of the force layout, which are hard-coded in the java script part of the html. The current, default choices are: distanceMin(20).distanceMax(150).strength(-20))

Warning: At the moment the script is **very** sensitive with author names. Thus, "Feynman, Richard" and "Feynman, Richard P." and "Feynman, Richard P" are all considered to be different authors.

Note: In general the python code is not optimised for performance but rather for readability, such that people can alter the code to fit it their custom purposes. Frankly, this seemed reasonable because the number of publications is usually << \infty

Advice: When you are creating the visualisations locally some browsers (Chrome and Safari) do not allow the loading of the external d3 library or your .json file. When you see only the headings but no illustration this is likely the case. Either, use Firefox (recommended), create a local server, or debug all the code online. When you upload the .html everything works fine with the other browsers, too.

If there are problems, please open an issue on the GitHub page.
