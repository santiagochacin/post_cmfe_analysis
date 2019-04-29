import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt

def import_test():
	print ('imported!')
	return()

def align_and_return_ezTrack(tracking_df, timestamps_df_path):

	timestamps_df = pd.read_table(timestamps_df_path)

	# timestamps of msCam and behavCam
	msCam_timestamps = timestamps_df[timestamps_df['camNum'] == 0].set_index('frameNum')
	behavCam_timestamps = timestamps_df[timestamps_df['camNum'] == 1].set_index('frameNum')

	# length to align is length of tracking df
	behav_trimmed = behavCam_timestamps.loc[:len(tracking_df)]

	# this produces a data frame with frame by frame tracking info from ezTrack 
	behav_trimmed['Distance'] = np.array(tracking_df['Distance'])

	# add following parameters to msCam data frame
	sys_clocks_behavCam = [0]
	behavCam_frames = [1]
	dist_btw_frames = [0]
	velocity = [0]

	# need to check alignemnt of new series here
	for msCam_frame in tqdm(range(2, len(msCam_timestamps)+1)):
		#get sys clock time of each miniscope recorded frame
		#find closest behav cam frame by sys clock time, 
		sys_clock_msCam = msCam_timestamps['sysClock'].loc[msCam_frame]
		behavCam_frame = list(behav_trimmed.iloc[(behav_trimmed['sysClock']-sys_clock_msCam).abs().argsort()[:1]].index)[0]
		behavCam_frames.append(behavCam_frame)
		sys_clocks_behavCam.append(behav_trimmed.loc[behavCam_frame]['sysClock'])
		delta_d = behav_trimmed.loc[behavCam_frame]['Distance']
		dist_btw_frames.append(delta_d)
		#velocity is the difference in the distance between frames divived by the sysClcok difference
		delta_t = behav_trimmed.loc[behavCam_frame]['sysClock']-behav_trimmed.loc[behavCam_frame-1]['sysClock']
		velocity.append(delta_d/(delta_t/1000))

	# add final values to df
	msCam_timestamps['velocity'] = velocity
	msCam_timestamps['Distance'] = dist_btw_frames
	msCam_timestamps['behavCam_frames'] = behavCam_frames
	msCam_timestamps['sys_clocks_behavCam'] = sys_clocks_behavCam

	return(msCam_timestamps)





#input timestamp data from miniscope DAQ and behaviorsoft tracking data


def align_and_return(tracking_df_path, timestamps_df_path):

	tracking_df = pd.read_table(tracking_df_path, header=None, names=['dist_btw_frames'])

	timestamps_df = pd.read_table(timestamps_df_path)

	# set tracking data frame index to frame numbers
	len(tracking_df)
	new_index = np.array([i for i in range(1, len(tracking_df)+1)])
	tracking_df['frameNum'] = pd.Series(new_index)
	tracking_df = tracking_df.set_index('frameNum')

	# timestamps of msCam and behavCam
	msCam_timestamps = timestamps_df[timestamps_df['camNum'] == 0]
	behavCam_timestamps = timestamps_df[timestamps_df['camNum'] == 1].set_index('frameNum')

	# length to align is length of tracking df
	behav_trimmed = behavCam_timestamps.loc[:len(tracking_df)]

	# this produces a data frame with frame by frame tracking info from behavior soft 
	behav_trimmed['dist_btw_frames'] = tracking_df['dist_btw_frames']

	msCam_timestamps = msCam_timestamps.set_index('frameNum')

	# add following parameters to msCam data frame
	sys_clocks_behavCam = [1]
	behavCam_frames = [1]
	dist_btw_frames = [0]
	velocity = [0]

	# need to check alignemnt of new series here
	for msCam_frame in tqdm(range(1, len(msCam_timestamps))):
		sys_clock_msCam = msCam_timestamps['sysClock'].loc[msCam_frame]
		behavCam_frame = list(behav_trimmed.iloc[(behav_trimmed['sysClock']-sys_clock_msCam).abs().argsort()[:1]].index)[0]
		behavCam_frames.append(behavCam_frame)
		sys_clocks_behavCam.append(behav_trimmed.loc[behavCam_frame]['sysClock'])
		delta_d = behav_trimmed.loc[behavCam_frame]['dist_btw_frames']
		dist_btw_frames.append(delta_d)
		#velocity is the difference in the distance between frames divived by the sysClcok difference
		delta_t = behav_trimmed.loc[behavCam_frame]['sysClock']-behav_trimmed.loc[behavCam_frame-1]['sysClock']
		velocity.append(delta_d/(delta_t/1000))

	# add final values to df
	msCam_timestamps['velocity'] = velocity
	msCam_timestamps['dist_btw_frames'] = dist_btw_frames
	msCam_timestamps['behavCam_frames'] = behavCam_frames
	msCam_timestamps['sys_clocks_behavCam'] = sys_clocks_behavCam

	return(msCam_timestamps)