import networkx as nx
from networkx.algorithms import bipartite
import pandas as pd
import argparse
import re
pd.set_option('mode.chained_assignment', None)

# parse the command line info
DEFAULT = dict(subcol='none', subname='none', entity='none', minweight=0, proj_name='NERtwork', out='csv')
parser = argparse.ArgumentParser(description='NERtwork')
parser.add_argument('-i', required=True)
parser.add_argument('-subcol', action="store", type=str, default=DEFAULT['subcol'])
parser.add_argument('-subname', action="store", type=str.lower, default=DEFAULT['subname'])
parser.add_argument('-entity', action="store", type=str.lower, default=DEFAULT['entity'])
parser.add_argument('-minweight', action="store", type=int, default=DEFAULT['minweight'])
parser.add_argument('-proj_name', action="store", default=DEFAULT['proj_name'])
parser.add_argument('-out', action="store", type=str.lower, default=DEFAULT['out'])
args = parser.parse_args()

# strip quotation marks from subname if used
if subname[0] in ("'", '"') and subname[-1] in ("'", '"'):
    subname=subname.strip("\'")
    subname=subname.strip('\"')
else:
    pass

def input_validator(batchner, subcol, subname, entity, minweight, proj_name, out):
    '''This checks each of the arguments taken by the parser. It also adds the subset term to the project name, if there is one.'''
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
    
    # checks to make sure the out is an acceptable option
    if out in ('csv', 'gexf'):
        pass
    else:
        print("The out parameter is unrecognized. Potential options are 'csv' or 'gexf'")
        exit()
    
    # return the project name, updated if needed
    return (proj_name)

def add_id(batchner, subcol, subname):
    '''This adds an id and entity label to the existing batchner dataframe. It also conducts a subset search, if there is one..'''
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

def create_projected_graph(batchnerID, minweight, entityType):
    '''Creates a projected graph and saves the edges as a dataframe.'''
    # create empty multigraph - multigraph is an undirected graph with parallel edges
    G = nx.MultiGraph()
    # import edge dataframe and create network
    G = nx.from_pandas_edgelist(batchnerID, source='doc', target='id', edge_attr=True)
    # project the graph onto entities, removing documents from the graph
    projected_graph = bipartite.weighted_projected_graph(G, batchnerID.id)
    if minweight!=0:
        projected_graph=nx.Graph( [ (u,v,d) for u,v,d in projected_graph.edges(data=True) if d['weight']>minweight] )
    else:
        pass
    for col in ('label', 'entityType'):
        node_atts = dict(zip(batchnerID.id, batchnerID[col],))
        nx.set_node_attributes(projected_graph, node_atts, col)
    return(projected_graph)

def create_csv(projected_graph, batchnerID, entityType, minweight, proj_name):
    '''Takes the projected graph and creates node and edge lists'''
    # convert the projected edge list
    edgelist = nx.to_pandas_edgelist(projected_graph)
    # creates a list of all unique nodes in the edgelist
    nodes=pd.DataFrame({'id':edgelist['source'].append(edgelist['target']).drop_duplicates()})
    # takes each node and looks up the corresponding labels
    nodelist = pd.merge(nodes[['id']],
                       batchnerID[['id','label', 'entityType']],
                       on='id'
    )
    nodelist = nodelist.drop_duplicates().reset_index(drop=True)

    # if there's a weight filter, include in file name; if not, don't include weight in filename
    if len(edgelist) >1:
        if minweight!= 0:
            # print node and edgelists to csv
            edgelist.to_csv(proj_name + '_ner_' + entityType + '_proj_edges_freq' + str(minweight) + '.csv', index=False)
            nodelist.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes_freq' + str(minweight) + '.csv', index=False)
        else:
            # print node & edgelist to csv
            edgelist.to_csv(proj_name + '_ner_' + entityType + '_proj_edges.csv', index=False)
            nodelist.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes.csv', index=False)
    else:
        print('No ' + entityType + ' edges met the minimum weight requirement')

def create_gexf(projected_graph, proj_name, entityType, minweight):
    '''Saves the projected graph as a gexf file'''
    if projected_graph.number_of_edges() != 0:    
        if minweight!=0:
            nx.write_gexf(projected_graph, proj_name + '_ner_' + entityType + '_proj_freq' + str(minweight) + '.gexf')
        else:
            nx.write_gexf(projected_graph, proj_name + '_ner_' + entityType + '_proj.gexf')
    else:
        print('No ' + entityType + ' edges met the minimum weight requirement')

def create_networks(batchneroutput, subcol, subname, entity, minweight, proj_name, out):
    '''Creates a loop based on entity filtering. In each loop, constructs a projected graph and distributes to the desired output. '''
    
    # loads a batchner output csv as a dataframe
    batchner=pd.read_csv(batchneroutput, low_memory=False)

    # makes sure all flags are valid and updates project name if needed
    proj_name=input_validator(batchner, subcol, subname, entity, minweight, proj_name, out)
 
    # set up loop to run on one or multiple entities
    if entity == 'all':
        entitylist = ['all', 'person', 'organization', 'location']
    # set none to all entity type
    elif entity =='none':
        entitylist=['all']
    # set entity list to specified single entity
    else:
        entitylist=[entity]   
    # loop through list of entityTypes desired
    for entityType in entitylist:
        # add id number to entities and filter for entitytype and subset
        if entityType == 'all':
            batchnerID=add_id(batchner, subcol, subname)
        else:
            batchnerID=add_id(batchner.loc[batchner['entityType'] == entityType], subcol, subname)
        
        # create a projected graph
        projected_graph=create_projected_graph(batchnerID, minweight, entityType)
        
        # send to appropriate output
        if out=='csv':
            create_csv(projected_graph, batchnerID, entityType, minweight, proj_name)
        elif out=='gexf':
            create_gexf(projected_graph, proj_name, entityType, minweight)
        else:
            pass

create_networks(args.i, args.subcol, args.subname, args.entity, args.minweight, args.proj_name, args.out)
