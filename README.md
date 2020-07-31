# NERtwork

## Overview

NERtwork is a collection of scripts to help you create a network graph of co-occurring named entities using open source tools. This is done by using Stanford Named Entity Recognizer to identify named entities in the documents, then using NetworkX to create a [bipartite projected network](https://en.wikipedia.org/wiki/Bipartite_network_projection), which is exportable in different formats..

Software required:

* [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml)
* [Anaconda](https://www.anaconda.com/) (strongly recommended, especially for Windows - includes the following 3 requirements, which can be installed separately)
	* [Python 3](https://www.python.org/)
	* [Pandas](https://pandas.pydata.org/)
	* [NetworkX](https://networkx.github.io/)
* [Cygwin](https://www.cygwin.com/install.html) (Windows only)
* [OpenRefine](https://openrefine.org/)
* Any network visualization software ([Palladio](https://hdlab.stanford.edu/palladio/) is great for beginners or basic exploration, [Gephi](https://gephi.org/) is recommended for more experienced users, or for more extensive research project. Anything that will accept an edge and node CSV will work, including Cytoscape, D3.js, or Flourish).

### Process
*More detailed steps are provided in the sections below*

1. Run [batchner.sh](#batchnersh) over a folder of text files. It will create a spreadsheet with a count of every named entity in every document in the folder.
2. [Optional, but *strongly* encouraged] Use [OpenRefine](https://openrefine.org/) or spreadsheet software to normalize, or correct and combine, entities that are the same (e.g. New York, NY, N.Y.). This will *significantly* improve your results.
3. [Required if you completed step 2] Run [batchner-collapse.py](#batchner-collapsepy) to consolidate duplicate entities creating by refinement.
4. [Optional] Join any relevant metadata so that you may subset the collection based on archival series, author, year, or whatever other metadata is useful. 
5. Run [batchner-to-network.py](#batchner-to-networkpy) to perform a bipartite network projection and save the resulting node and edge lists.
6. Import node and edge lists into network visualization software of your choice!

## batchner.sh

This is a single command-line script that will call the Stanford Named Entity Recognizer on each text file in a folder, count unique entities, and print the results into a spreadsheet.

The final spreadsheet (called entities.csv) will have the text filename, the entity recognized, the type of entity (organization, location, person), and the number of times that each entity occurred as that type within the document. _Note: It's possible for the same word to be tagged as more than one type of entity within a document._

### Requirements
This script only works on text (.txt) files, but it will work on as many text files as you'd like without any further interaction on your part.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download) and rename the folder `stanford-ner`, and also [the batchner.sh script](https://github.com/brandontlocke/NERtwork/blob/master/batchner.sh). **Do not forget to rename the folder (or edit the .sh file or this will not work.**

### Folder Setup
As is, the script will run Stanford NER on every text (.txt) file within a folder. This expects that all of the text files and the batchner.sh script are all within the same folder, and that the stanford-ner folder is in the same directory as the folder of files. **Make sure you have renamed the stanford-ner folder**

(Note: you do not have to change the names of the .txt files—the filenames below are just for demonstration)

```
├──🗂 stanford-ner
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
The purpose of renaming the stanford-ner folder is that every new version has a different folder name, meaning this script needs to be updated every few months with every new Stanford NER release. Changing the folder name on your hard drive means that this script needs significantly less maintenance.

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
2. In a command line window (Terminal for Mac, Anaconda for Windows), navigate to the directory with your batcher-to-network.py file and type `python batchner-collapse.py path/to/your/refined/batchner/file`
3. The resulting spreadsheet with merged and re-counted entities will append `_refined` to the end of the filename.

*Thank you to Devin Higgins for creating this script*

### Adding metadata
At this point, it may be beneficial to include any relevant metadata you may have about your documents so that you may subset the collection based on archival series, author, year, or whatever other metadata is useful. This will vary greatly on the metadata you have, but you can look to the [Fannie Lou Hamer Papers metadata join script](https://github.com/FannieLouHamerPapers/code/blob/master/flh-metadatamerge.py) or [the Illinois Library's OpenRefine's join tutorial](https://guides.library.illinois.edu/openrefine/joiningprojects) as examples. 

The next script allows limited subsetting (explained below), but for more complex needs, you may need to create separate batchner CSV files using [OpenRefine's faceting](https://github.com/OpenRefine/OpenRefine/wiki/Cell-Editing#editing-through-text-facets) or custom Python [Py example](https://github.com/FannieLouHamerPapers/code/blob/master/flh-series-split.py).

## batchner-to-network.py

Takes a batchner output, creates a [bipartite projected network](https://en.wikipedia.org/wiki/Bipartite_network_projection) of named entity co-occurrences, and saves them in your desired file format. In other words, it counts the co-occurrence of named entities within a set of documents and represents them as connected nodes in a network.

### Requirements
* Anaconda (or NetworkX, Pandas, Python)
* A batchner output

### Options
* `-i` [**REQUIRED**] sets the location of the batchner file you want to construct a network from
* `-proj_name` [recommended] allows you to give your project a name that will be at the beginning of the filename. (default = nertwork)
* `-subcol` [optional] specifies the column you want to use to create a subset. This is case-sensitive. If you use subcol, you must also use subname. (default = none)
* `-subname` [optional; required if subcol used] searches in the subcol for a character, word or phrase to create a subset of the data. If your search term includes spaces or special characters put quotes or double quotes on each side of the term. The search string is also included in the filename, if used. (default = none)
* `-entity` [optional] allows you to limit your network to only specific types of networks (default = none)
	* `none` will create a network. including all types of entities, 
	* `person`, `location`, or `organization` will create a network of only that type of entity
	* `all` will create 4 networks: all types, person, location, and organization.
* `-minweight` [optional] will filter out entity relationships with weights below a specified number. This filter is applied at the end of the process, so projection is done based on the complete list, and the output is filtered by the projected weight. This can be helpful in really large graphs. (default = 0)
* `-out` [optional] will determine what type of output files you want (default = csv)
	* `csv` creates two csvs—an edge list and a node list
	* `gexf` creats a GEXF (Graph Exchange XML Format) file

### Subsetting
You can create networks from subsets of the data using `subcol` to select a column and `subname` to facet on characters in that column. Although this will technically work on any column, this is likely not helpful unless you have joined additional data, or want to use a segment of information from the doc name.
* `subcol` must perfectly match (including case) the name of the column. 
* `subname` is a case-insensitive literal string search that only needs to match on part of a field in a dataset. (Ex: `-subname=correspondence` will match 'Correspondence: Letter to J. Smith' as well as 'Memo: Regarding earlier correspondence')
* If you have spaces or special characters, add single or double quotes to your argument (note: some special characters will still cause problems and you may need to your metadata or use another method for subsetting)
* Your search term will be stripped of spaces and special characters (if any) and added to the final filename.
* Warning: If the data in the `subcol` column is not a string, it will be converted to a string for matching. This also means that, for the time being at least, you cannot search for numbers above/below a point or dates before/after a date.
* If you want to facet on multiple terms or in multiple columns, if you have special characters you need to find, or you need to facet on something other than a string, I recommend using spreadsheet software, OpenRefine, or Python to create alternative subset data to use.
* **This is a brand new feature and has not been tested very much. If you've run into a problem that isn't described above, or have a recommended solution to improve this, please file an issue**

### Instructions
1. Save the [batchner-to-network.py file](https://github.com/brandontlocke/NERtwork/blob/master/batchner-to-network.py) to your machine
2. In a command line window (Terminal for Mac, Anaconda for Windows), navigate to the directory with your batchner-to-network.py file and type `python batchner-to-network.py -i=path/to/your/batchner/file`, plus any other flags you may want

#### Examples
* `python batchner-to-network.py -i=data/my_dataset.csv -proj_name=my_dataset -subset=person -minweight=5` 
	* this will run on a file named "my_dataset.csv" that's in the data folder within your current directory, it will add a "my_dataset_" prefix to every file it creates, it will only run the network on shared person names, and it will only save nodes and edges with a weight of over 5
* `python batchner-to-network.py -i=https://gist.githubusercontent.com/brandontlocke/f568ffdeaf7fdb17e27872916645591b/raw/f1a28d05ce2a4cdbbe11c09404cdf83c7a5fb1c1/inaugural-batchner -proj_name=inauguralspeeches`
	* this will take a batchner output file from Github, prefix every file with 'inauguralspeeches_', and will include all entities. **this file is available on the web, so feel free to run tests with this command**

