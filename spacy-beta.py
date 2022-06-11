import spacy
import pandas as pd
import os
#load this spaCy model-will need to come up with a better way to load this in
nlp = spacy.load('en_core_web_sm')
#create empty DataFrame with column heads
entities=pd.DataFrame(columns=['doc', 'entity', 'entityType', 'count'])

for file in os.listdir():
    # run spaCy entity recognizer on each .txt document
    if file.endswith(".txt"):
        doctext  = open(file).read()
        docnlp = nlp(doctext)
        doclist=pd.DataFrame(columns=['entity', 'entityType',])
        for ent in docnlp.ents:
            if ent.label_ == 'LOC' or ent.label_ == 'GPE':
                doclist = doclist.append({'entity': ent.text, 'entityType':'location'}, ignore_index=True)
            elif ent.label_ == 'PERSON':
                doclist = doclist.append({'entity': ent.text, 'entityType':'person'}, ignore_index=True)
            elif ent.label_ == 'ORG':
                doclist = doclist.append({'entity': ent.text, 'entityType':'organization'}, ignore_index=True)
        #sort list and combine counts for the same entity
        doclist = doclist.groupby(doclist.columns.tolist()).size().reset_index().rename(columns={0:'count'})
        #add a column with the document name
        doclist.insert(0, 'doc', file)
        #append results from this document to a list of all documents
        entities = entities.append(doclist)
entities.to_csv('entities.csv', index=False)
