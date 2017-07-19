#Regulatory Graph Analysis

#Libraries
from __future__ import division
import json
import pandas as pd
from py2neo import Node, Relationship, Graph
import re
import math
import string
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import sys
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.cluster import KMeans,AgglomerativeClustering, MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import normalize
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
             discriminant_analysis, random_projection)
from features import get_regulatory_networks, get_genes
from tensor import AutoEncoder

#Function to create centrality features for the Nodes in the Regulatory Network
def create_features(graph):
	#Nodes in the regulatory network
	genes = graph.nodes()

	#In Degree Centrality
	in_degree = nx.in_degree_centrality(graph)

	#Out Degree Centrality
	out_degree = nx.out_degree_centrality(graph)

	#Closeness Centrality
	closeness = nx.closeness_centrality(graph)

	#Betweeness centrality -- Fraction of all-pairs shortest path that passes through a given network
	node_betweenness = nx.betweenness_centrality(graph)

	#Edge Betweenness - To find important edges in the network
	edge_betweenness = nx.edge_betweenness_centrality(graph)

	#Page Rank for node ranking values
	page_rank = nx.pagerank(graph,alpha=0.8)

	#Dictionary for storing features for each gene
	feature_dictionary = {}

	#Populate with Genes and Features
	for gene in genes:
		#Initialization
		feature_dictionary[gene] = []

		#In Degree
		feature_dictionary[gene].append(in_degree[gene])

		#Out Degree
		feature_dictionary[gene].append(out_degree[gene])

		#Closeness
		feature_dictionary[gene].append(closeness[gene])

		#Node Betweenness
		feature_dictionary[gene].append(node_betweenness[gene])

		#Page Rank
		feature_dictionary[gene].append(page_rank[gene])


	return feature_dictionary


	

#Function to create features for nodes in the Regulatory Graph
def regulatory_analysis():
	#Connection to Neo4j
	graph = Graph("http://localhost:7474/db/data/cypher",password="rimo")

	#Get a list of Genes and their corresponding length
	genes, lengths = get_genes(graph)

	#Get the regulatory network
	regulatory_network = get_regulatory_networks(graph,genes)

	#Initializing instance for Directed NetworkX Graph
	g = nx.DiGraph()

	#Conversion into list of tuples
	edge_list = map((lambda x : (x[0],x[1])),regulatory_network)

	#Addition of edges into the directed graph
	g.add_edges_from(edge_list)

	#Creation of features for the nodes
	node_features = create_features(g)

	#Feature List
	feature_list = []

	for gene in node_features:
		feature_list.append(node_features[gene])


	#Conversion into numpy array
	feature_array = np.array(feature_list)

	weights, biases = AutoEncoder(feature_array)

	print weights
	print biases




	




regulatory_analysis()
