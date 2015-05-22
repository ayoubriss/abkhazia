"""
@author Roland Thiolliere
"""

"""
This script contains functions to train an ABnet for a list of pairs of same words
and to calculate the embeddings using a trained ABnet.
"""

import os.path as p
import os
from abnet.run import run
import abnet.prepare as prepare
from abnet.layers import Linear, ReLU, SigmoidLayer, SoftPlus
from abnet.nnet_archs import ABNeuralNet2Outputs
from abnet.stack_fbanks import stack_fbanks
import cPickle
import numpy as np
import h5features


def train(same_pair_file, output_path,

          n_layers=2, same_word_ratio=0.5,
          same_speaker_ratio=None,
          train_ratio=0.7,
          feature_type='fbanks',
          verbose=0):
    """
    Function to train an ABnet on a list of words

    It takes as input a list of pairs of same words. This file contains several lines in the format:
    wav1 start1 stop1 wav2 start2 stop2 spk-id1 spk-id2
    - wav1 and wav2 are wavefiles specified with their full path
    - start1, start2, stop1, stop2 are times in seconds
    - spk-id1 and spk-id2 are strings identifying uniquely the speakers

    Parameters:
        same_pair_file: string
            path to the input file. This file contains a list of pairs of same words.
	output_path: string
        n_layers: int
            number of hidden layers of the neural network
        same_word_ratio: float
            ratio "number of same word pairs" / "total number of pairs" for each training batch. Default to 0.5
        same_speaker_ratio: float
            ratio "number of same speaker pairs" / "total number of pairs" for each training batch. Default to the initial ratio
        train_ratio: float
            proportion of the data used for training (the rest are used for validation, to avoid overfitting)
        feature_type: string
    """
    pairs_file = p.join(output_path, 'pairs.joblib')
    features_file = p.join(output_path, 'fb.h5f')

    # prepare.run(same_pair_file, pairs_file, features_file)
    dataset_path = pairs_file
    dataset_name = p.splitext(pairs_file)[0]
    run(dataset_path=dataset_path, dataset_name=dataset_name,
        batch_size=100, nframes=7, features='fbank',
        init_lr=0.01, max_epochs=500, 
        network_type='AB', trainer_type='adadelta',
        layers_types=[SigmoidLayer] * (n_layers + 1),
        layers_sizes=[500] * n_layers,
        loss='cos_cos2',
        prefix_fname='',
        debug_print=verbose,
        debug_time=verbose,
        debug_plot=False,
        mv_file=dataset_name + "_mean_std.npz",
        mm_file=dataset_name + "_min_max.npz",
        train_ratio=train_ratio,
    )


def decode(model_path, wavefile_list, output_file,

           verbose=0):
    """
    Function to calculate the embeddings for a list of wavefiles using a trained ABnet
    in the h5features format

    Parameters:
        model_path: string, path to the abnet
        wavefile_list: string, path to the list of wavefiles (wavefiles are specified by their full path, one file per line)
        output_file: string, path to the outputfile, it will contains the embeddings in h5features format
    """
    with open(wavefile_list) as fin:
        wavefiles = [w.strip() for w in fin]
    nnet_file = p.join(model_path, 'pairs_fbank7_AB_adadelta_emb_100.pickle')
    mean_std_file = p.join(model_path, 'pairs_mean_std.npz')
    stacked_fb_file = p.join(model_path, 'stackedfb.h5f')
    # prepare.h5features_fbanks(wavefiles, stacked_fb_file,
    #                           featfunc=lambda f: stack_fbanks(prepare.do_fbank(p.splitext(f)[0])))
    if verbose:
        print('stacked fbanks calculated')
    with open(nnet_file, 'rb') as f:
        nnet = cPickle.load(f)

    NFRAMES = 7

    transform = nnet.transform_x1()
    tmp = np.load(mean_std_file)
    mean = np.tile(tmp['mean'], NFRAMES)
    std = np.tile(tmp['std'], NFRAMES)

    if verbose:
        print('model loaded')

    index = h5features.read_index(stacked_fb_file)
    # TODO maybe normalize embedded features ???
    def do_transform(fname):
        times, feats = h5features.read(stacked_fb_file, from_internal_file=fname,
                                       index=index)
        times = times[fname]
        feats = feats[fname]
        X = np.asarray((feats - mean) / std, dtype='float32')
        # times = np.arange(0.01, 0.01*npz.shape[0], 0.01)
        emb_wrd, emb_spkr = transform(X)
        return emb_wrd
    prepare.h5features_fbanks(index['files'], output_file, featfunc=do_transform)
    if verbose:
        print('bottleneck features calculated, all done.')
    
