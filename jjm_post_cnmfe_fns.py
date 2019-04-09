import sys
import os
import glob
import importlib
import multiprocessing as mp

from matplotlib import pyplot as plt
import scipy.sparse as sparse
import scipy.io as sio
import scipy.stats as stats
import scipy.spatial.distance as dist
import numpy as np
import h5py
from tqdm import tqdm
import pandas as pd
import tables

sys.path.append('/Users/johnmarshall/Documents/MATLAB/CNMF_E/python_wrapper/')
sys.path.append('/Users/johnmarshall/caiman_data/demos/notebooks/post_cnmfe_analysis')
import python_utils as utils


def get_neuron_pairs(num_neurons):
	#create list of tuples for neuron pairs
	neuron_pairs = []
	for i in range(num_neurons):
		for j in range(num_neurons):
			if i != j: 
				neuron_pairs.append((i,j))
	return(neuron_pairs)


def get_r_coeffs_distances_paired(neuron_pairs, matresults_C, coordinates):
	pairwise = {}
	for pair in tqdm(neuron_pairs):
	#calculate pearsons r
		r = stats.pearsonr(matresults_C[pair[0]], matresults_C[pair[1]])
	#calc euclidian distance 
		distance = dist.euclidean(coordinates[pair[0]]['CoM'], coordinates[pair[1]]['CoM'])
		pairwise[pair] = (r, distance)
	return(pairwise)

def get_pairwise_comparisons(data_path_folder):
	# Load up all processed files found in base directory
	results_names = [] # Name of folders where results were saved
	compiled_results = {}
	pairwise_results = {}
	for f_name in glob.glob(data_path_folder + '*/*/*/''out.mat'):
		name = f_name.split(os.sep)[-4]
		compiled_results[name] = sio.loadmat(f_name) # Loaded mat files containing CNMF-E output
		results_names.append(name) # Name of folders where results were saved
		print(name)
		# Call contour plotting function from Caiman (with our results from MATLAB!)
		coordinates = utils.plot_contours(compiled_results[name] ['A'].todense(), 
													compiled_results[name] ['Cn'],
													display_numbers=False, maxthr=.6,
													cmap='gray', colors='r')
		#create list of tuples for neuron pairs
		neuron_pairs = get_neuron_pairs(len(coordinates))
		#get pairwise comparisons
		pairwise_distances_pearsons_r = get_r_coeffs_distances_paired(neuron_pairs, compiled_results[name]['C'], coordinates)
		#ultimately convert to df and save output
		pairwise_df = pd.DataFrame(pairwise_distances_pearsons_r)
		pairwise_df.to_hdf(data_path_folder + name + 'pairwise_comparisons.h5', key='df', mode='w', complevel=5)
		pairwise_results[name] = pairwise_distances_pearsons_r
	return(pairwise_results)
