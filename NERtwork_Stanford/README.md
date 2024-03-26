# NERtwork_Stanford

## Overview

This folder contains the deprecated documentation and batch shell script for using Stanford NER with NERtwork. All steps described in the spaCy NERtwork documentation are the same, except for the batchner process.

Software required:

* [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml)

## batchner.sh

This is a single command-line script that will call the Stanford Named Entity Recognizer on each text file in a folder, count unique entities, and print the results into a spreadsheet.

The final spreadsheet (called entities.csv) will have the text filename, the entity recognized, the type of entity (organization, location, person), and the number of times that each entity occurred as that type within the document. _Note: It's possible for the same word to be tagged as more than one type of entity within a document._

### Requirements
This script only works on text (.txt) files, but it will work on as many text files as you'd like without any further interaction on your part.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download) and rename the folder `stanford-ner`, and also [the batchner.sh script](https://github.com/brandontlocke/NERtwork/blob/master/batchner.sh). **Do not forget to rename the folder (or edit the .sh file or this will not work.**

### Options
* `-s` [required for Windows, optional for Mac/Unix] specifies what kind of operating system you're using. Options are 'unix' (Mac, Linux, Windows Subsystem for Linux) or 'win' for Windows. (default = unix)
* `-l` specifies language — right now eng is the only option. (default = eng)
* `-d` [optional] specifies the directory where the text files are. If you don't use it, it will run on .txt files in the current working directory. Can be a relative or absolute path, and should end in a slash. (default = '') *see Default Folder Setup for more info*
* `-n` [optional] specifies the directory where `ner.sh` and `stanford-ner.jar` are. If you don't use it, it will look for a folder named `stanford-ner` on directory above the current working directory. Can be a relative or absolute path, and should end in a slash. (default = '../stanford-ner/') *see Default Folder Setup for more info*

### Default Folder Setup
As is, the script will run Stanford NER on every text (.txt) file within a folder. This expects that all of the text files and the batchner.sh script are all within the same folder, and that the `stanford-ner` folder is in the same directory as the folder of files. **Make sure you have renamed the stanford-ner folder**

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

### Running the Script
#### Mac OS X
Once all of your files are properly arranged as above:
1. Open Terminal
2. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project_folder' on the Desktop, type (without the $) `$ cd Desktop/project_folder`.]
3. Type `$ sh batchner.sh` and then any of the optional options listed above
This will take a bit to run (it should generally do 4-5 files per minute, depending on the length of the document), but will print all of the results into a file in the same folder called `entities.csv`

### Windows
Download and install [Cygwin](https://www.cygwin.com/install.html). Once your files are arranged as above:
1. Open Cygwin
2. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project_folder' on the Desktop, type (without the $) `$ cd /cygdrive/c/Users/YOUR-USERNAME/Desktop/project_folder`, making sure to insert your Windows user name into the YOUR-USERNAME space.]
3. Type `$ sh batchner.sh -s win` and then any of the optional options listed above
This will take a bit to run (it should generally do 4-5 files per minute, depending on the length of the document), but will print all of the results into a file in the same folder called `entities.csv`

### Notes
The purpose of renaming the stanford-ner folder is that every new version has a different folder name, meaning this script needs to be updated every few months with every new Stanford NER release. Changing the folder name on your hard drive means that this script needs significantly less maintenance.

This would not have have been possible without Bill Turkel's [Named Entity Recognition with Command Line Tools in Linux](https://williamjturkel.net/2013/06/30/named-entity-recognition-with-command-line-tools-in-linux/)
