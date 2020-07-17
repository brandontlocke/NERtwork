# NERtwork

## Overview

NERtwork is a collection of scripts to help you create a network graph of co-occurring named entities using open source tools. This is done by using Stanford Named Entity Recognizer to identify named entities in the documents, then using NetworkX to create a [bipartite projected network](https://en.wikipedia.org/wiki/Bipartite_network_projection) and exporting the node and edge lists for use in network visualization tools.

Software required:

* [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml)
* [Python 3](https://www.python.org/)\*
* [Pandas](https://pandas.pydata.org/)\*
* [NetworkX](https://networkx.github.io/)\*
* [Cygwin](https://www.cygwin.com/install.html) (Windows only)
* [OpenRefine](https://openrefine.org/)
* Any network visualization software ([Palladio](https://hdlab.stanford.edu/palladio/) is great for beginners or basic exploration, [Gephi](https://gephi.org/) is recommended for more experienced users, or for more extensive research project. Anything that will accept an edge and node CSV will work, including Cytoscape, D3.js, or Flourish).
	\* Python, Pandas, and NetworkX are all installed by default with [Anaconda](https://www.anaconda.com/).

### Process
*More detailed steps are provided in the sections below*

1. Run [batchner.sh](#batchnersh) over a folder of text files. It will create a spreadsheet with a count of every named entity in every document in the folder.
2. Use [OpenRefine](https://openrefine.org/) or spreadsheet software to normalize, or correct and combine, entities that are the same (e.g. New York, NY, N.Y.). This step is optional, but will *significantly* improve your results.
3. Run [batchner-collapse.py](#batchner-collapsepy) to consolidate duplicate entities creating by refinement. Only use this if you completed step 2.
4. Run [batchner-to-network.csv](#batchner-to-networkcsv) to perform a bipartite network projection and save the resulting node and edge lists.
5. Import node and edge lists into network visualization software of your choice!

## batchner.sh

This is a single command-line script that will call the Stanford Named Entity Recognizer on each text file in a folder, count unique entities, and print the results into a spreadsheet.

The final spreadsheet (called entities.csv) will have the text filename, the entity recognized, the type of entity (organization, location, person), and the number of times that each entity occurred as that type\* within the document.

\*It's possible for the same word to be tagged as more than one type of entity within a document.

### Requirements
This script only works on text (.txt) files, but it will work on as many text files as you'd like without any further interaction on your part.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download) and also [the batchner.sh script](https://github.com/brandontlocke/NERtwork/blob/master/batchner.sh).

### Folder Setup
As is, the script will run Stanford NER on every text (.txt) file within a folder. This expects that all of the text files and the batchner.sh script are all within the same folder, and that the NER folder (as of this writing, the `stanford-ner-4.0.0`) is in the same directory as the folder of files. 

(Note: you do not have to change the names of the .txt files—the filenames below are just for demonstration)

```
├──🗂 stanford-ner-4.0.0
├──🗂 project_folder
|   └──batchner.sh
|   └──file1.txt
|   └──file2.txt
|   └──file3.txt
|   └──file4.txt
|   └──file5.txt
|   └──file6.txt
|   └──etc.
```
If you're familiar with shell scripting and file navigation, you can fairly easily change the script and arrange the files however you would like.

### Running the Script
#### Mac OS X
Once all of your files are properly arranged as above:
1. Open Terminal
2. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project_folder' on the Desktop, type (without the $) `$ cd Desktop/project_folder`.]
3. Type `$ sh batchner.sh`
This will take a bit to run (it should generally do 4-5 files per minute), but will print all of the results into a file in the same folder called `entities.csv`

### Windows
Download and install [Cygwin](https://www.cygwin.com/install.html). Once your files are arranged as above:
1. Open batchner.sh in a text editor, remove the `#` at the start of line 8 (starts with `nertext=$(java -mx600m -cp`...), and add a `#` to line 9 (starts with `nertext=$(stanford-ner`...)
2. Open Cygwin
3. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project_folder' on the Desktop, type (without the $) `$ cd /cygdrive/c/Users/YOUR-USERNAME/Desktop/project_folder`, making sure to insert your Windows user name into the YOUR-USERNAME space.]
4. Type `$ sh batchner.sh`
This will take a bit to run (it should generally do 4-5 files per minute), but will print all of the results into a file in the same folder called `entities.csv`

### Notes
As new versions of Stanford NER come out, the folder name will change and you may need to update your batchner.sh file so that portion of text on lines 8 or 9 that say `stanford-ner-X.X.X` match the folder name

This would not have have been possible without Bill Turkel's [Named Entity Recognition with Command Line Tools in Linux](https://williamjturkel.net/2013/06/30/named-entity-recognition-with-command-line-tools-in-linux/)

## Refining the entity list

### Requirements
* [OpenRefine](https://openrefine.org/) (not absolutely required, but strongly recommended)
* Python 3
* A batchner output

### Normalizing entities

You may find a number of entities that mean the same thing, but are spelled or represented differently. For example, you may know that "B. Obama" and "Barack Obama" are the same person, or that "Chicago, Illinois", "Chicago", and "Chicago, IL" all refer to the same place. You'll likely want to edit those to make them all the same. If you have a really small dataset, you may be able to edit them in spreadsheet software, but I'd strongly recommend using [OpenRefine](https://openrefine.org/) to locate potential duplicates and edit in bulk. You'll likely want to use the [text facet](https://github.com/OpenRefine/OpenRefine/wiki/Cell-Editing#editing-through-text-facets) and [clustering](https://github.com/OpenRefine/OpenRefine/wiki/Clustering) features. 

Once that is done, you'll likely have some duplicate data. For example, you may decide to normalize all variations of Chicago to just "Chicago". If "Chicago, IL" is used once in a document and "Chicago" is also used once, you will be left with two identical rows saying Chicago was used once in the document.

### batchner-collapse.py
This Python script will save you the time of finding all of these duplicates and adding the counts together. 

1. Save [batchner-collapse.py](https://github.com/brandontlocke/NERtwork/blob/master/batchner-collapser.py) to your machine
2. In a terminal window, navigate to the directory with your batcher-to-network.py file and type `python batchner-collapse.py path/to/your/batchner/file`
3. The resulting spreadsheet with merged and re-counted entities will append `_refined` to the end of the filename.

*Thank you to Devin Higgins for creating this script*

## batchner-to-network.csv

Takes a batchner output, creates a [bipartite projected network](https://en.wikipedia.org/wiki/Bipartite_network_projection) of named entity co-occurrences, and saves node and edge lists as CSV. In other words, it counts the co-occurrence of named entities within a set of documents and represents them as connected nodes in a network.

### Requirements
* [NetworkX](https://networkx.github.io/)
* [Pandas](https://pandas.pydata.org/)
* Python 3
* A batchner output

### Options
* `-i` [**REQUIRED**] sets the location of the batchner file you want to construct a network from
* `-proj_name` [recommended] allows you to give your project a name that will be at the beginning of the filename. (default = nertwork)
* `-subset` [optional] allows you to limit your network to only specific types of networks (default = none)
	* `none` will create a network. including all types of entities, 
	* `person`, `location`, or `organization` will create a network of only that type of entity
	* `all` will create 4 networks: all types, person, location, and organization. 
* `-minweight` [optional] will filter out entity relationships with weights below a specified number. This can be helpful in really large graphs. (default = 0)


### Instructions
1. Save the [batchner-to-network.py file](https://github.com/brandontlocke/NERtwork/blob/master/batchner-to-network.py) to your machine
2. In a terminal window, navigate to the directory with your batchner-to-network.py file and type `python batchner-to-network.py -i=path/to/your/batchner/file`, plus any other flags you may want

#### Examples
* `python batchner-to-network.py -i=data/my_dataset.csv -proj_name=my_dataset -subset=person -minweight=5` 
	* this will run on a file named "my_dataset.csv" that's in the data folder within your current directory, it will add a "my_dataset_" prefix to every file it creates, it will only run the network on shared person names, and it will only save nodes and edges with a weight of over 5
* `python batchner-to-network.py -i=https://gist.githubusercontent.com/brandontlocke/f568ffdeaf7fdb17e27872916645591b/raw/f1a28d05ce2a4cdbbe11c09404cdf83c7a5fb1c1/inaugural-batchner -proj_name=inauguralspeeches`
	* this will take a batchner output file from Github, prefix every file with 'inauguralspeeches_', and will include all entities. **this file is available on the web, so feel free to run tests with this command**

