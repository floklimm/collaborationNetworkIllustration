# collaboration_network
Creating interactive visualisations of collaboration networks with JavaScript

This allows the creation of visulisations of your scientific collaboration network with the D3.js library. Input is a BibTex library file with all (your) publications. It works by calling the python script {\t bibtex2json}, which writes a .json. The JSON is then read by html/js to create the illustration.

Requirements:
  - python for the script running
  - python module pybtex for reading the BibTex file
  - D3, which will be loaded automatically by your browser when it is needed

Howto:
  - save your publications into a bibfile, e.g. MarieCurie.bib
  - edit the python file bibtex2json.py to read your input file and also choose an appropriate outputfile name , e.g., MarieCurie.json
  - run bibtex2json.py
  - 


Advice: When you are creating the visualisations locally some browsers (Chrome and Safari) do not allow the loading of the external d3 lirbary or your .json file. When you see only the headings but no illustration this is likely the case. Either, use Firefox (recommended), create a local server, or debug all the code online.

If there are problems, please open an issue on the GitHub page.
