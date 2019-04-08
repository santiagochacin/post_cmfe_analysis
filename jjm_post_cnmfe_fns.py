import scipy.sparse as sparse
import scipy.io as sio
import scipy.stats as stats
import scipy.spatial.distance as dist
import numpy as np
from tqdm import tqdm


def get_neuron_pairs(num_neurons):
	#create list of tuples for neuron pairs
	neuron_pairs = []
	for i in range(len(coordinates)):
		for j in range(len(coordinates)):
			if i != j: 
			neuron_pairs.append((i,j))
	return()


def get_r_coeffs_distances_paired(neuron_pairs, C, coordinates):
	pairwise = {}
	for pair in tqdm(neuron_pairs):
    #calculate pearsons r
    	r = stats.pearsonr(mat_results['C'][pair[0]], mat_results['C'][pair[1]])
    #calc euclidian distance 
    	distance = dist.euclidean(coordinates[pair[0]]['CoM'], coordinates[pair[1]]['CoM'])
    	pairwise[pair] = (r, distance)
	return(pairwise)