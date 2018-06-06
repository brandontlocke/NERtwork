Batch script for Named Entity Recognition

## Folder Setup
This script, as is, will run Stanford NER on every text file within a folder. This expects that the stanford-ner-2018-02-27 folder, all of the text files, and the batchner.sh script are all within the same folder.

── project folder  
├── stanford-ner-2018-02-27  
├── file1.txt  
├── file2.txt  
├── file1.txt  
├── file2.txt  
├── batchner.sh

## Running the Script
In terminal, navigate to the folder containing these files and type `sh batchner.sh`. This will take a bit to run, but will print all of the results into a file called `entities.csv`

## Notes
As new versions of Stanford NER come out, the filepath will change and will need to be updated
