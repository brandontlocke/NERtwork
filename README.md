# Batch script for Named Entity Recognition

This is a single command-line script that will call the Stanford Named Entity Recognizer on each text file in a folder, count unique entities, and print the results into a spreadsheet.

The final spreadsheet (called entities.csv) will have the text filename, the entity recognized, the type of entity (organization, location, person), and the number of times that entity occurred as that type** within the document.

\**It's possible for the same word to be tagged as more than one type of entity within a document.

## Requirements
At the moment, this only works on a Mac OSX machine.

This script only works on text (.txt) files, but it will work on as many text files as you'd like without any futher interaction on your part.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download)

## Folder Setup
As is, the script will run Stanford NER on every text (.txt) file within a folder. This expects that the stanford-ner-2018-02-27 folder, all of the text files, and the batchner.sh script are all within the same folder.

```
├──🗂  project folder
|   ├──🗂 stanford-ner-2018-02-27
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
Once all of your files are properly arranged, open Terminal, navigate to the folder containing these files (using `$ cd`) and type `$ sh batchner.sh`. This will take a bit to run (4-5 files will likely take about a minute), but will print all of the results into a file in the same folder called `entities.csv`

## Notes
As new versions of Stanford NER come out, the filepath will change and will need to be updated
