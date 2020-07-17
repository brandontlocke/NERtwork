import networkx as nx
from networkx.algorithms import bipartite
import pandas as pd
import argparse

# parse the command line info
DEFAULT = dict(subset='none', minweight=0, proj_name='nertwork')
parser = argparse.ArgumentParser(description='Test app')
parser.add_argument('-i', required=True)
parser.add_argument('-subset', action="store", default=DEFAULT['subset'])
parser.add_argument('-minweight', action="store", type=int, default=DEFAULT['minweight'])
parser.add_argument('-proj_name', action="store", default=DEFAULT['proj_name'])
args = parser.parse_args()

def addID(batchner):
    '''This adds an id and entity label to the existing batchner dataframe. Requires a batchner output.'''
    # create a list of all unique entities in the set
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

def edgesFromProjectedGraph(batchnerID):
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

def getNodeLabels(edgelist, batchnerID):
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

def createNetwork(batchnerlist, subset='none', minweight=0, proj_name='nertwork'):
    '''Creates a projected network from batchner output and optionall filters by entitytype and minimum weight. Subset options are 'none', all', 'person', 'location', 'organization'. Subset will default to only making the full graph. Minweight will accept any number from 0 to 99999999.'''    
    # loads a batchner output csv as a dataframe
    batchner=pd.read_csv(batchnerlist, low_memory=False)
    # checks to see if minweight is a reasonable number
    if minweight in range(0,99999999):
        pass
    else:
        print("The minweight parameter is not a number, or is too high.")
    
    # checkes to make sure the subset is an acceptable option
    if subset == 'none' or 'all' or 'person' or 'location' or 'organization':
        pass
    else:
        print("The subset parameter is unrecognized. Potential options are 'none', 'all', 'person', 'location', 'organization'")
    
    # check to see if a full graph should be created
    if subset == 'none' or 'all':
        batchnerID=addID(batchner)
        edgelist = edgesFromProjectedGraph(batchnerID)

        # if there's a weight filter, check edge weight and print; otherwise, print them all
        if minweight!= 0:
            # filter 
            filtered_edges=edgelist.loc[edgelist.weight >= minweight]
            filtered_nodes=getNodeLabels(filtered_edges, batchnerID)
            # make sure something met the minweight
            if len(filtered_edges) < 2:
                print('No edges met the minimum weight requirement')
            else:
                # print node & edgelist to csv
                filtered_edges.to_csv(proj_name+'_ner_all_proj_edges_freq'+ str(minweight) + '.csv', index=False)
                filtered_nodes.to_csv(proj_name+'_ner_all_proj_nodes_freq'+ str(minweight) + '.csv', index=False)
        else:
            # print node & edgelist to csv
            edgelist.to_csv(proj_name+'_ner_full_proj_edges.csv', index=False)
            nodelist = getNodeLabels(edgelist, batchnerID)
            nodelist.to_csv(proj_name+'_ner_full_proj_nodes.csv', index=False)
        
    else:
        pass
    
    # if all subsets are being created, enter into a loop
    if subset == 'all':
        # provide all three subsets for the loop
        entitylist = ['person', 'organization', 'location']        
        for entityType in entitylist:
            batchnerID=addID(batchner.loc[batchner['entityType'] == entityType])
            edgelist = edgesFromProjectedGraph(batchnerID)
            
            # if there's a weight filter, check edge weight and print; otherwise, print them all
            if minweight!= 0:
                # filter 
                filtered_edges=edgelist.loc[edgelist.weight >= minweight]
                filtered_nodes=getNodeLabels(filtered_edges, batchnerID)
                # make sure something met the minweight
                if len(filtered_edges) < 2:
                    print('No ' + entityType + ' edges met the minimum weight requirement')
                else:
                    # print node and edgelists to csv
                    filtered_edges.to_csv(proj_name + '_ner_' + entityType + '_proj_edges_freq' + str(minweight) + '.csv', index=False)
                    filtered_nodes.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes_freq' + str(minweight) + '.csv', index=False)
            else:
                # print node & edgelist to csv
                edgelist.to_csv(proj_name + '_ner_' + entityType + '_proj_edges.csv', index=False)
                nodelist = getNodeLabels(edgelist, batchnerID)
                nodelist.to_csv(proj_name + '_ner_' + entityType + '_proj_nodes.csv', index=False) 
      
    # if only one subset is being created, filter and run through
    elif subset == 'person' or 'location' or 'organization':
        batchnerID=addID(batchner.loc[batchner['entityType'] == subset])
        edgelist=edgesFromProjectedGraph(batchnerID)
        
        # if there's a weight filter, check edge weight and print; otherwise, print them all
        if minweight!= 0:
            #filter
            filtered_edges=edgelist.loc[edgelist.weight >= minweight]
            filtered_nodes=getNodeLabels(filtered_edges, batchnerID)
            # make sure something met the minweight
            if len(filtered_edges) < 2:
                print('No ' + subset + ' edges met the minimum weight requirement')
            else:
                #print node and edgelists to csv
                filtered_edges.to_csv(proj_name+'_ner_' + subset + '_proj_edges_freq'+ str(minweight) + '.csv', index=False)
                filtered_nodes.to_csv(proj_name+'_ner_' + subset + '_proj_nodes_freq'+ str(minweight) + '.csv', index=False)
        else:
            #print node & edge list to csv
            edgelist.to_csv(proj_name+ '_ner_' + subset + '_proj_edges.csv', index=False)
            nodelist = getNodeLabels(edgelist, batchnerID)
            nodelist.to_csv(proj_name+ '_ner_' + subset + '_proj_nodes.csv', index=False)    
    else:
        pass
    
createNetwork(args.i, args.subset, args.minweight, args.proj_name)
