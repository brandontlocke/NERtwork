# Batch script for Named Entity Recognition

This is a single command-line script that will call the Stanford Named Entity Recognizer on each text file in a folder, count unique entities, and print the results into a spreadsheet.

The final spreadsheet (called entities.csv) will have the text filename, the entity recognized, the type of entity (organization, location, person), and the number of times that entity occurred as that type** within the document.

\**It's possible for the same word to be tagged as more than one type of entity within a document.

## Requirements
This script only works on text (.txt) files, but it will work on as many text files as you'd like without any further interaction on your part.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download) and also [script in this repository](https://github.com/brandontlocke/batchner/blob/master/batchner.sh).

## Folder Setup
As is, the script will run Stanford NER on every text (.txt) file within a folder. This expects that all of the text files and the batchner.sh script are all within the same folder, and that the NER folder (as of this writing, the `stanford-ner-2018-10-16`) is in the same directory as the folder of files. 

(Note: you do not have to change the names of the .txt files—the filenames below are just for demonstration)

```
├──🗂 stanford-ner-2018-10-16
├──🗂 project folder
|   └──batchner.sh
|   └──file1.txt
|   └──file2.txt
|   └──file3.txt
|   └──file4.txt
|   └──file5.txt
|   └──file6.txt
|   └──etc.
```
If you're familiar with shell scripting and file navigation, you can fairly easily restructure this.

## Running the Script
### Mac OS X
Once all of your files are properly arranged as above:
1. Open Terminal
2. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project' on the Desktop, type (without the $) `$ cd Desktop/project`.]
3. Type `$ sh batchner.sh`
This will take a bit to run (4-5 files will likely take about a minute), but will print all of the results into a file in the same folder called `entities.csv`

### Windows
Download and install [Cygwin](https://www.cygwin.com/install.html). Once your files are arranged as above:
1. Open batchner.sh in a text editor, remove the `#` at the start of line 8 (starts with `nertext=$(java -mx600m -cp`...), and add a `#` to line 9 (starts with `nertext=$(stanford-ner`...)
2. Open Cygwin
3. Navigate to the folder containing these files (using `$ cd`) [if you have a folder 'project' on the Desktop, type (without the $) `$ cd /cygdrive/c/Users/YOUR-USERNAME/Desktop/project`.]
4. Type `$ sh batchner.sh`
This will take a bit to run (4-5 files will likely take about a minute), but will print all of the results into a file in the same folder called `entities.csv`

## Notes
As new versions of Stanford NER come out, the filepath will change and will need to be updated

This would have have been possible without Bill Turkel's [Named Entity Recognition with Command Line Tools in Linux](https://williamjturkel.net/2013/06/30/named-entity-recognition-with-command-line-tools-in-linux/)
