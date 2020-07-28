import networkx as nx
from networkx.algorithms import bipartite
import pandas as pd
import argparse
import re
pd.set_option('mode.chained_assignment', None)

# parse the command line info
DEFAULT = dict(subcol='none', subname='none', entity='none', minweight=0, proj_name='NERtwork')
parser = argparse.ArgumentParser(description='Test app')
parser.add_argument('-i', required=True)
parser.add_argument('-subcol', action="store", type=str, default=DEFAULT['subcol'])
parser.add_argument('-subname', action="store", type=str.lower, default=DEFAULT['subname'])
parser.add_argument('-entity', action="store", type=str.lower, default=DEFAULT['entity'])
parser.add_argument('-minweight', action="store", type=int, default=DEFAULT['minweight'])
parser.add_argument('-proj_name', action="store", default=DEFAULT['proj_name'])
args = parser.parse_args()

def input_validator(batchner, subcol, subname, entity, minweight, proj_name):
    # checks to see if minweight is a reasonable number
    if minweight in range(0,99999999):
        pass
    else:
        print("The minweight parameter is not a number, or is too high.")
        exit()
    
    # if subset is not none, makes sure the column exists
    if subcol =='none':
        pass
    elif subcol in list(batchner.columns.values):
        # if there is a subcol, make sure it exists in the data and then make sure there's a subname that also matches
        pass
        # makes sure the subset name exists within the subset column, if one is specified
        if subname in str(batchner[subcol].values).lower():
            # strip spaces and characters from subname and append to proj_name so that final files with have subset information in them
            # this is a lazy way to add this name to the files, but it prevents me from adding if/else statements in like 10 places and doubling the number of lines
            cleansubname=re.sub('[^A-Za-z0-9]+', '', subname)
            proj_name=proj_name + '_' + cleansubname    
        else:
            print("The subname does not exist in the subcol, or you have not entered a subname. Please check your data and make sure everything is spelled correctly.")
            exit()
    else:
        print("The subcol does not exist in the dataset. This option is case-sensitive. Options are")
        for col in (batchner.columns.values):
            print(col)
        exit()
   
    # checks to make sure the entity is an acceptable option
    if entity in ('none', 'all', 'person', 'location', 'organization'):
        pass
    else:
        print("The entity parameter is unrecognized. Potential options are 'none', 'all', 'person', 'location', 'organization'")
        exit()
    
    # return the project name, updated if needed
    return (proj_name)


def add_id(batchner, subcol, subname):
    '''This adds an id and entity label to the existing batchner dataframe. Requires a batchner output.'''
    # create a list of all unique entities in the set
    if subcol=='none':
        pass
    else:
        if batchner[subcol].dtypes != str:
            batchner[subcol]=batchner[subcol].apply(str)
        else:
            pass
        batchner=batchner.loc[batchner[subcol].str.contains(subname, flags=re.IGNORECASE, regex=False)]
    nodes=batchner[['entity', 'entityType']].drop_duplicates().reset_index(drop=True)
    # create a dataframe of each entity with a unique numbered identifier
    nodes_list = pd.DataFrame({'id': nodes.index, 'label': nodes.entity, 'entityType': nodes.entityType})
    # merge dataframes together so each entity has an ID assigned to it
    batchnerID = pd.merge(batchner[['doc','entity','entityType','count']],
                       nodes_list[["id", 'label', 'entityType']],
                       left_on=['entity', 'entityType'],
                       right_on=['label', 'entityType']
    )
    return(batchnerID)

def edges_from_projected_graph(batchnerID):
    '''Creates a projected graph and saves the edges as a dataframe.'''
    # create empty multigraph - multigraph is an undirected graph with parallel edges
    G = nx.MultiGraph()
    # import edge dataframe and create network
    G = nx.from_pandas_edgelist(batchnerID, source='doc', target='id', edge_attr=True)
    # project the graph onto entities, removing documents from the graph
    full_graph = bipartite.weighted_projected_graph(G, batchnerID.id)
    # convert the projected edge list
    edgelist = nx.to_pandas_edgelist(full_graph)
    return(edgelist)

def get_node_labels(edgelist, batchnerID):
    '''Creates a dataframe of nodes with desired metadata. Expects an edgelist and listing of node ids/labels'''
    # creates a list of all unique nodes in the edgelist
    nodes=pd.DataFrame({'id':edgelist['source'].append(edgelist['target']).drop_duplicates()})
    # takes each node and looks up the corresponding labels
    nodes_labels = pd.merge(nodes[['id']],
                       batchnerID[['id','label', 'entityType']],
                       on='id'
    )
    nodes_labels = nodes_labels.drop_duplicates().reset_index(drop=True)
    return(nodes_labels)

def create_network(batchneroutput, subcol, subname, entity, minweight, proj_name):
    '''Creates a projected network from batchner output and optional filters by subset, entitytype and minimum weight. Subset searches for subname in subcol. Entity options are 'none', all', 'person', 'location', 'organization'. Entity will default to only making the full graph. Minweight will accept any number from 0 to 99999999.'''    
    
    # loads a batchner output csv as a dataframe
    batchner=pd.read_csv(batchneroutput, low_memory=False)

    # makes sure all flags are valid and updates project name if needed
    proj_name=input_validator(batchner, subcol, subname, entity, minweight, proj_name)
 
    # provide all three entities plus all for the loop 
    if entity == 'all':
        entitylist = ['all', 'person', 'organization', 'location']
    # set none to all entity types
    elif entity =='none':
        entitylist=['all']
    # set entity list to specified single entity
    else:
        entitylist=[entity]   
    # loop through list and create edge lists for each entity
    for entityType in entitylist:
        if entityType == 'all':
            batchnerID=add_id(batchner, subcol, subname)
        else:
            batchnerID=add_id(batchner.loc[batchner['entityType'] == entityType], subcol, subname)
        edgelist = edges_from_projected_graph(batchnerID)
        
        # if there's a weight filter, select by edge weight and print; otherwise, print them all
        if minweight!= 0:
            # filter 
            filtered_edges=edgelist.loc[edgelist.weight >= minweight]
            filtered_nodes=get_node_labels(filtered_edges, batchnerID)
            # make sure something met the minweight
            if len(filtered_edges) < 2:
                print('No ' + entityType + ' edges met the minimum weight requirement')
                exit()
            else:
                # print node and edgelists to csv
                filtered_edges.to_csv(proj_name + '_ner_' + entityType + '_proj_edges_freq' + str(minweight) + '.csv', index=False)
                filtered_nodes.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes_freq' + str(minweight) + '.csv', index=False)
        else:
            # print node & edgelist to csv
            edgelist.to_csv(proj_name + '_ner_' + entityType + '_proj_edges.csv', index=False)
            nodelist = get_node_labels(edgelist, batchnerID)
            nodelist.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes.csv', index=False) 

create_network(args.i, args.subcol, args.subname, args.entity, args.minweight, args.proj_name)