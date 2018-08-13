# Batch script for Named Entity Recognition

## Requirements
At the moment, this only works on a Mac OSX machine.

This will need 1 or more text file (ending in .txt) to work.

You will need to download [Stanford Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml#Download)

## Folder Setup
This script, as is, will run Stanford NER on every text (.txt) file within a folder. This expects that the stanford-ner-2018-02-27 folder, all of the text files, and the batchner.sh script are all within the same folder.

```
├── project folder
|   ├── stanford-ner-2018-02-27
|   └── batchner.sh
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
In terminal, navigate to the folder containing these files and type `sh batchner.sh`. This will take a bit to run, but will print all of the results into a file in the same folder called `entities.csv`

## Notes
As new versions of Stanford NER come out, the filepath will change and will need to be updated
