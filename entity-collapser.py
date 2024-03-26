# script created by Devin Higgins, adapted by Brandon Locke

import csv
import sys

if len(sys.argv) != 2:
    raise ValueError('Please provide a batchner file')

batchner = sys.argv[1]

with open(batchner, "rU") as csvfile:
  csv_reader = csv.DictReader(csvfile)

  for row in csv_reader:
    print(row)

# Sample data structure.
data_structure = {
    "text": {
        "type": {
            "entity": 0
        },
    },
}

data = {}

with open(batchner, "rU") as csvfile:
  csv_reader = csv.DictReader(csvfile)

  for row in csv_reader:
    doc = row["doc"]
    entity = row["entity"]
    entityType = row["entityType"]
    count = int(row["count"])
    
    if doc in data:
      
      if entityType in data[doc]:
        
        if entity in data[doc][entityType]:
          
          data[doc][entityType][entity] += count
          
        else:
          
          data[doc][entityType][entity] = count
          
      else:
          
          data[doc][entityType] = {entity: count}
          
    else:
      
      data[doc] = {
          
          entityType: {
            entity: count      
          }
        }

      print(data)

rows = []

# These must match the row keys below.
fieldnames = ["doc", "entity", "entityType", "count"]

for doc in data:

  for entityType in data[doc]:

    for entity in data[doc][entityType]:

      row = {
          # The keys here must match the fieldnames specified above.
          "doc": doc,
          "entity": entity,
          "count": data[doc][entityType][entity],
          "entityType": entityType,
      }
      rows.append(row)

        
with open(sys.argv[1].replace('.csv', '_refined.csv'), "w") as csvoutput:
  csv_writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
  csv_writer.writeheader()
  for row in rows:
    csv_writer.writerow(row)