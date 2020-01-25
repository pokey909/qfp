#!/usr/bin/env python
# -*- coding: utf_8 -*-

from qfp import QueryFingerprint
from qfp.db import QfpDB
import numpy as np
import concurrent.futures
import fnmatch
import os
import sqlite3
from pydub import AudioSegment


def load_audio(path, downsample=False, normalize=False, target_dBFS=-20.0, snip=None):
    """
    Creates array of samples from input audio file
    snip = only return first n seconds of input
    """
    audio = AudioSegment.from_file(path)
    if downsample:
        # if stereo, sample rate > 8kHz, or > 16-bit depth
        if (audio.channels > 1) \
                or (audio.frame_rate != 8000) \
                or (audio.sample_width != 2):
            audio = _downsample(audio)
    if normalize and audio.dBFS is not target_dBFS:
        audio = _normalize(audio, target_dBFS)
    """if snip > audio.duration_seconds:
        raise InvalidAudioLength(
            "Provided snip length is longer than audio file")"""
    if snip is not None:
        milliseconds = snip * 1000
        audio = audio[:milliseconds]
    return audio


def _downsample(audio, numChannels=1, sampleRate=8000, bitDepth=2):
    """
    Returns downsampled AudioSegment
    """
    audio = audio.set_channels(numChannels)
    audio = audio.set_frame_rate(sampleRate)
    audio = audio.set_sample_width(bitDepth)
    return audio


def _normalize(audio, target_dBFS):
    """
    Normalizes loudness of AudioSegment
    """
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def slidingWindow(sequence,winSize,step=1, seed=987):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Verify the inputs
    try:
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    # set the seed for the pseudo-random number generator
    np.random.seed(seed)

    # Pre-compute number of chunks to emit
    numOfChunks = int(((len(sequence)-winSize)/step)+1)

    # Create a shuffled index of start points
    idx = np.arange(numOfChunks)
    # np.random.shuffle(idx)

    # Do the work
    for i in range(0, numOfChunks*step, step):
        start_idx = i
        stop_idx = i + winSize
        yield sequence[start_idx:stop_idx]


def find_matches(snippet, start, end):
    snippet.export("unknown_audio.wav")
    db = QfpDB()
    fp_q = QueryFingerprint("unknown_audio.wav")
    fp_q.create()
    db.query(fp_q, vThreshold=0.1)
    print("Pos: " + str(start) + " / " + str(end))
    print(fp_q.matches)

def main():
    snippet_length_seconds = 15 * 1000
    audio = load_audio("data/mixotic/mixes/data/set044/Mixotic_044_-_Cotumo_-_Pentagonik_Labelmix_2006-06-27.mp3")
    start = 0
    end = snippet_length_seconds
    step = snippet_length_seconds
    for win in slidingWindow(audio, snippet_length_seconds, step):
        find_matches(win, start, end)
        start += step
        end = start + snippet_length_seconds


if __name__ == '__main__':
    main()
